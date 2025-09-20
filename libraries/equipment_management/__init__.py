"""
Equipment Management Library for 123erfasst MCP Server

This library provides equipment management functionality for construction projects.
Follows Article I: Library-First Principle - Standalone library for equipment management.
"""

from .equipment_manager import EquipmentManager
from .exceptions import EquipmentManagementError, EquipmentNotFoundError, InvalidEquipmentDataError

__all__ = [
    "EquipmentManager",
    "EquipmentManagementError",
    "EquipmentNotFoundError",
    "InvalidEquipmentDataError"
]
