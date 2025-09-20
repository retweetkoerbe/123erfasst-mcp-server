"""
Unit tests for GraphQL client library.

Follows Article III: Test-First Imperative - Tests written before implementation.
"""
import pytest
import httpx
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libraries"))

from graphql_client import GraphQLClient, GraphQLClientError, AuthenticationError, NetworkError, DataError


class TestGraphQLClient:
    """Test cases for GraphQLClient class."""
    
    def test_init_with_valid_credentials(self):
        """Test client initialization with valid credentials."""
        client = GraphQLClient("https://test.api.com", "test-token")
        assert client.base_url == "https://test.api.com"
        assert client.token == "test-token"
        assert client.username == "api"  # Default username
        assert "Authorization" in client.headers
        # Check that Basic Auth is properly encoded
        import base64
        expected_encoded = base64.b64encode(b"api:test-token").decode('utf-8')
        assert client.headers["Authorization"] == f"Basic {expected_encoded}"
    
    def test_init_with_empty_token_raises_error(self):
        """Test that empty token raises AuthenticationError."""
        with pytest.raises(AuthenticationError):
            GraphQLClient("https://test.api.com", "")
    
    def test_init_with_none_token_raises_error(self):
        """Test that None token raises AuthenticationError."""
        with pytest.raises(AuthenticationError):
            GraphQLClient("https://test.api.com", None)
    
    def test_init_with_custom_username(self):
        """Test client initialization with custom username."""
        client = GraphQLClient("https://test.api.com", "test-token", "custom-user")
        assert client.base_url == "https://test.api.com"
        assert client.token == "test-token"
        assert client.username == "custom-user"
        assert "Authorization" in client.headers
        # Check that Basic Auth is properly encoded with custom username
        import base64
        expected_encoded = base64.b64encode(b"custom-user:test-token").decode('utf-8')
        assert client.headers["Authorization"] == f"Basic {expected_encoded}"
    
    @pytest.mark.asyncio
    async def test_query_success(self):
        """Test successful GraphQL query execution."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"test": "success"},
            "errors": None
        }
        
        with patch("httpx.AsyncClient.post", return_value=mock_response):
            result = await client.query("query { test }")
            assert result == {"test": "success"}
    
    @pytest.mark.asyncio
    async def test_query_with_variables(self):
        """Test GraphQL query with variables."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"project": {"id": "123", "name": "Test Project"}},
            "errors": None
        }
        
        with patch("httpx.AsyncClient.post", return_value=mock_response):
            result = await client.query(
                "query GetProject($id: ID!) { project(id: $id) { id name } }",
                {"id": "123"}
            )
            assert result["project"]["id"] == "123"
            assert result["project"]["name"] == "Test Project"
    
    @pytest.mark.asyncio
    async def test_query_authentication_error(self):
        """Test query with authentication error."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errors": [{"message": "Unauthorized"}]
        }
        
        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(AuthenticationError):
                await client.query("query { test }")
    
    @pytest.mark.asyncio
    async def test_query_network_error(self):
        """Test query with network error."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        with patch("httpx.AsyncClient.post", side_effect=httpx.NetworkError("Network error")):
            with pytest.raises(NetworkError):
                await client.query("query { test }")
    
    @pytest.mark.asyncio
    async def test_query_graphql_errors(self):
        """Test query with GraphQL errors in response."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": None,
            "errors": [{"message": "Field 'invalid' doesn't exist"}]
        }
        
        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(DataError):
                await client.query("query { invalid }")
    
    @pytest.mark.asyncio
    async def test_mutation_success(self):
        """Test successful GraphQL mutation execution."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"createProject": {"id": "123", "name": "New Project"}},
            "errors": None
        }
        
        with patch("httpx.AsyncClient.post", return_value=mock_response):
            result = await client.mutation(
                "mutation CreateProject($name: String!) { createProject(name: $name) { id name } }",
                {"name": "New Project"}
            )
            assert result["createProject"]["id"] == "123"
            assert result["createProject"]["name"] == "New Project"
    
    @pytest.mark.asyncio
    async def test_retry_logic_on_transient_error(self):
        """Test retry logic on transient network errors."""
        client = GraphQLClient("https://test.api.com", "test-token")
        
        # First call fails, second succeeds
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {
            "data": {"test": "success"},
            "errors": None
        }
        
        with patch("httpx.AsyncClient.post", side_effect=[mock_response_fail, mock_response_success]):
            result = await client.query("query { test }")
            assert result == {"test": "success"}
    
    def test_headers_include_content_type(self):
        """Test that headers include proper content type."""
        client = GraphQLClient("https://test.api.com", "test-token")
        assert client.headers["Content-Type"] == "application/json"
    
    def test_headers_include_authorization(self):
        """Test that headers include authorization."""
        client = GraphQLClient("https://test.api.com", "test-token")
        assert "Authorization" in client.headers
        assert client.headers["Authorization"].startswith("Basic ")
