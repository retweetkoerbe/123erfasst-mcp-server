"""
Custom exceptions for time tracking operations.

Follows Article V: Error Handling and Resilience - Categorize errors for proper handling.
"""

class TimeTrackingError(Exception):
    """Base exception for time tracking errors."""
    pass

class InvalidProjectError(TimeTrackingError):
    """Raised when project ID is invalid or project doesn't exist."""
    pass

class TimeTrackingActiveError(TimeTrackingError):
    """Raised when trying to start time tracking when already active."""
    pass

class TimeTrackingNotActiveError(TimeTrackingError):
    """Raised when trying to stop time tracking when not active."""
    pass

class InvalidPersonError(TimeTrackingError):
    """Raised when person ID is invalid or person doesn't exist."""
    pass
