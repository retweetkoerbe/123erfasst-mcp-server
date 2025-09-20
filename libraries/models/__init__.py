"""
Data Models Library for 123erfasst MCP Server

This library provides Pydantic models for all 123erfasst entities.
Follows Article VIII: Anti-Abstraction Principle - Use single model representation for each entity.
"""

from .project import Project
from .staff_time import StaffTime
from .person import Person
from .equipment import Equipment
from .ticket import Ticket
from .planning import Planning
from .factories import ModelFactory

__all__ = [
    "Project",
    "StaffTime", 
    "Person",
    "Equipment",
    "Ticket",
    "Planning",
    "ModelFactory"
]
