"""
Project Management Library for 123erfasst MCP Server

This library provides project management functionality for construction projects.
Follows Article I: Library-First Principle - Standalone library for project management.
"""

from .project_manager import ProjectManager
from .exceptions import ProjectManagementError, ProjectNotFoundError, InvalidProjectDataError

__all__ = [
    "ProjectManager",
    "ProjectManagementError",
    "ProjectNotFoundError",
    "InvalidProjectDataError"
]
