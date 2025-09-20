"""
GraphQL Client Library for 123erfasst API

This library provides GraphQL client functionality for interacting with the 123erfasst API.
Follows Article IV: GraphQL-First API Design - All interactions use GraphQL as primary interface.
"""

from .client import GraphQLClient
from .exceptions import GraphQLClientError, AuthenticationError, NetworkError, DataError

__all__ = [
    "GraphQLClient",
    "GraphQLClientError", 
    "AuthenticationError",
    "NetworkError",
    "DataError"
]
