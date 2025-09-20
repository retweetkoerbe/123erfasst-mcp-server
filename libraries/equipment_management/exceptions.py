"""
Custom exceptions for equipment management operations.

Follows Article V: Error Handling and Resilience - Categorize errors for proper handling.
"""

class EquipmentManagementError(Exception):
    """Base exception for equipment management errors."""
    pass

class EquipmentNotFoundError(EquipmentManagementError):
    """Raised when equipment ID is invalid or equipment doesn't exist."""
    pass

class InvalidEquipmentDataError(EquipmentManagementError):
    """Raised when equipment data is invalid or incomplete."""
    pass

class EquipmentAssignmentError(EquipmentManagementError):
    """Raised when equipment assignment fails."""
    pass
