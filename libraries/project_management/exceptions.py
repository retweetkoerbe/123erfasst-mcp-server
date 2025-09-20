"""
Custom exceptions for project management operations.

Follows Article V: Error Handling and Resilience - Categorize errors for proper handling.
"""

class ProjectManagementError(Exception):
    """Base exception for project management errors."""
    pass

class ProjectNotFoundError(ProjectManagementError):
    """Raised when project ID is invalid or project doesn't exist."""
    pass

class InvalidProjectDataError(ProjectManagementError):
    """Raised when project data is invalid or incomplete."""
    pass

class ProjectAccessError(ProjectManagementError):
    """Raised when user doesn't have access to project."""
    pass
