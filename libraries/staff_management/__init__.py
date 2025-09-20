"""
Staff Management Library for 123erfasst MCP Server

This library provides staff management functionality for construction projects.
Follows Article I: Library-First Principle - Standalone library for staff management.
"""

from .staff_manager import StaffManager
from .exceptions import StaffManagementError, PersonNotFoundError, InvalidPersonDataError

__all__ = [
    "StaffManager",
    "StaffManagementError",
    "PersonNotFoundError",
    "InvalidPersonDataError"
]
