"""
CLI interface for GraphQL client testing.

Follows Article II: CLI Interface Mandate - All functionality accessible through CLI.
"""
import asyncio
import json
import sys
import argparse
from typing import Optional
from .client import GraphQLClient, GraphQLClientError
import logging

# Set up logger for CLI
logger = logging.getLogger(__name__)


async def test_connection(base_url: str, token: str) -> None:
    """Test connection to GraphQL API."""
    try:
        client = GraphQLClient(base_url, token)
        await client.test_connection()
        logger.info(f"✅ Successfully connected to GraphQL API")
    except Exception as e:
        logger.info(f"❌ Connection failed: {e}")
        sys.exit(1)


async def execute_query(base_url: str, token: str, query: str, variables: Optional[str] = None) -> None:
    """Execute a GraphQL query."""
    try:
        client = GraphQLClient(base_url, token)
        
        # Parse variables if provided
        vars_dict = None
        if variables:
            vars_dict = json.loads(variables)
        
        result = await client.query(query, vars_dict)
        logger.info(json.dumps(result, indent=2))
    except Exception as e:
        logger.info(f"❌ Query execution failed: {e}")
        sys.exit(1)


async def execute_mutation(base_url: str, token: str, mutation: str, variables: Optional[str] = None) -> None:
    """Execute a GraphQL mutation."""
    try:
        client = GraphQLClient(base_url, token)
        
        # Parse variables if provided
        vars_dict = None
        if variables:
            vars_dict = json.loads(variables)
        
        result = await client.mutation(mutation, vars_dict)
        logger.info(json.dumps(result, indent=2))
    except Exception as e:
        logger.info(f"❌ Mutation execution failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="GraphQL Client CLI")
    parser.add_argument("--base-url", required=True, help="GraphQL API base URL")
    parser.add_argument("--token", required=True, help="API authentication token")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test connection command
    subparsers.add_parser("test-connection", help="Test connection to GraphQL API")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Execute a GraphQL query")
    query_parser.add_argument("--query", required=True, help="GraphQL query string")
    query_parser.add_argument("--variables", help="JSON string of variables")
    
    # Mutation command
    mutation_parser = subparsers.add_parser("mutation", help="Execute a GraphQL mutation")
    mutation_parser.add_argument("--mutation", required=True, help="GraphQL mutation string")
    mutation_parser.add_argument("--variables", help="JSON string of variables")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "test-connection":
        asyncio.run(test_connection(args.base_url, args.token))
    elif args.command == "query":
        asyncio.run(execute_query(args.base_url, args.token, args.query, args.variables))
    elif args.command == "mutation":
        asyncio.run(execute_mutation(args.base_url, args.token, args.mutation, args.variables))


if __name__ == "__main__":
    main()
