"""
Custom exceptions for GraphQL client operations.

Follows Article V: Error Handling and Resilience - Categorize errors for proper handling.
"""

class GraphQLClientError(Exception):
    """Base exception for GraphQL client errors."""
    pass

class AuthenticationError(GraphQLClientError):
    """Raised when authentication fails."""
    pass

class NetworkError(GraphQLClientError):
    """Raised when network operations fail."""
    pass

class DataError(GraphQLClientError):
    """Raised when data validation or processing fails."""
    pass
