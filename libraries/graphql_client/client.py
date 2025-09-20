"""
GraphQL Client for 123erfasst API.

Follows Article IV: GraphQL-First API Design and Article V: Error Handling and Resilience.
"""
import asyncio
import base64
import json
import logging
from typing import Dict, Any, Optional
import httpx
from .exceptions import GraphQLClientError, AuthenticationError, NetworkError, DataError

logger = logging.getLogger(__name__)


class GraphQLClient:
    """
    GraphQL client for interacting with 123erfasst API.
    
    Follows Article VI: Security and Authentication - Secure credential management.
    Follows Article V: Error Handling and Resilience - Comprehensive error handling.
    """
    
    def __init__(self, base_url: str, token: str, username: str = None):
        """
        Initialize GraphQL client.
        
        Args:
            base_url: Base URL for the GraphQL endpoint
            token: API token for authentication (can be password or full token)
            username: Username for Basic Authentication (optional, defaults to 'api')
            
        Raises:
            AuthenticationError: If token is empty or None
        """
        if not token:
            raise AuthenticationError("API token is required")
        
        self.base_url = base_url
        self.token = token
        self.username = username or "api"  # Default username for 123erfasst API
        
        # Implement proper Basic Authentication as per RFC 7617
        # Format: username:password encoded in base64
        credentials = f"{self.username}:{self.token}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"GraphQL client initialized for {base_url} with Basic Auth")
    
    async def query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query.
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            Query result data
            
        Raises:
            AuthenticationError: If authentication fails
            NetworkError: If network operation fails
            DataError: If GraphQL returns errors
        """
        return await self._execute(query, variables, operation_type="query")
    
    async def mutation(self, mutation: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL mutation.
        
        Args:
            mutation: GraphQL mutation string
            variables: Optional variables for the mutation
            
        Returns:
            Mutation result data
            
        Raises:
            AuthenticationError: If authentication fails
            NetworkError: If network operation fails
            DataError: If GraphQL returns errors
        """
        return await self._execute(mutation, variables, operation_type="mutation")
    
    async def _execute(self, operation: str, variables: Optional[Dict[str, Any]], operation_type: str) -> Dict[str, Any]:
        """
        Execute GraphQL operation with retry logic.
        
        Follows Article V.2: Error Response - Implement retry logic for transient failures.
        """
        payload = {
            "query": operation,
            "variables": variables or {}
        }
        
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self.base_url,
                        headers=self.headers,
                        json=payload,
                        timeout=30.0
                    )
                    
                    # Handle HTTP errors
                    if response.status_code == 401:
                        raise AuthenticationError("Invalid or expired API token")
                    elif response.status_code >= 500:
                        if attempt < max_retries - 1:
                            logger.warning(f"Server error {response.status_code}, retrying in {retry_delay}s")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                            continue
                        else:
                            raise NetworkError(f"Server error after {max_retries} attempts: {response.status_code}")
                    elif response.status_code >= 400:
                        raise NetworkError(f"Client error: {response.status_code}")
                    
                    # Parse response
                    try:
                        data = response.json()
                    except json.JSONDecodeError as e:
                        raise DataError(f"Invalid JSON response: {e}")
                    
                    # Check for GraphQL errors
                    if "errors" in data and data["errors"]:
                        error_messages = [error.get("message", "Unknown error") for error in data["errors"]]
                        raise DataError(f"GraphQL errors: {'; '.join(error_messages)}")
                    
                    # Return data
                    if "data" not in data:
                        raise DataError("No data in GraphQL response")
                    
                    logger.debug(f"GraphQL {operation_type} executed successfully")
                    return data["data"]
                    
            except httpx.NetworkError as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Network error, retrying in {retry_delay}s: {e}")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise NetworkError(f"Network error after {max_retries} attempts: {e}")
            except (AuthenticationError, DataError):
                # Don't retry on auth or data errors
                raise
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Unexpected error, retrying in {retry_delay}s: {e}")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise GraphQLClientError(f"Unexpected error after {max_retries} attempts: {e}")
        
        # This should never be reached, but just in case
        raise GraphQLClientError("Maximum retries exceeded")
    
    async def test_connection(self) -> bool:
        """
        Test connection to the GraphQL API.
        
        Returns:
            True if connection is successful
            
        Raises:
            GraphQLClientError: If connection fails
        """
        try:
            # Simple introspection query to test connection
            await self.query("query { __schema { queryType { name } } }")
            logger.info("GraphQL connection test successful")
            return True
        except Exception as e:
            logger.error(f"GraphQL connection test failed: {e}")
            raise GraphQLClientError(f"Connection test failed: {e}")
