"""
Custom exceptions for staff management operations.

Follows Article V: Error Handling and Resilience - Categorize errors for proper handling.
"""

class StaffManagementError(Exception):
    """Base exception for staff management errors."""
    pass

class PersonNotFoundError(StaffManagementError):
    """Raised when person ID is invalid or person doesn't exist."""
    pass

class InvalidPersonDataError(StaffManagementError):
    """Raised when person data is invalid or incomplete."""
    pass

class PersonAccessError(StaffManagementError):
    """Raised when user doesn't have access to person data."""
    pass
