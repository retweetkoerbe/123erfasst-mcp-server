"""
Planning model for project planning and milestones.

Follows Article VIII: Anti-Abstraction Principle - Single model representation for Planning entity.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator


class Planning(BaseModel):
    """
    Project planning entity.
    
    Represents planning data, milestones, and resource allocations for projects.
    """
    id: str = Field(..., description="Unique planning record identifier")
    project_id: str = Field(..., description="Project identifier")
    milestone: Optional[str] = Field(None, description="Milestone or task name")
    planned_date: Optional[date] = Field(None, description="Planned completion date")
    actual_date: Optional[date] = Field(None, description="Actual completion date")
    status: Optional[str] = Field(None, description="Status (planned, in_progress, completed, delayed)")
    description: Optional[str] = Field(None, description="Detailed description")
    assigned_person_id: Optional[str] = Field(None, description="Assigned person ID")
    estimated_hours: Optional[float] = Field(None, description="Estimated hours to complete")
    actual_hours: Optional[float] = Field(None, description="Actual hours spent")
    dependencies: Optional[list[str]] = Field(None, description="List of dependent planning IDs")
    priority: Optional[str] = Field(None, description="Priority level (low, medium, high)")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Planning ID is required')
        return v.strip()
    
    @validator('project_id')
    def validate_project_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Project ID is required')
        return v.strip()
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ['planned', 'in_progress', 'completed', 'delayed', 'cancelled']
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None:
            valid_priorities = ['low', 'medium', 'high']
            if v not in valid_priorities:
                raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return v
    
    @validator('actual_date')
    def validate_actual_date(cls, v, values):
        if v and 'planned_date' in values and values['planned_date']:
            # Allow actual date to be different from planned date
            pass
        return v
    
    @validator('estimated_hours')
    def validate_estimated_hours(cls, v):
        if v is not None and v < 0:
            raise ValueError('Estimated hours cannot be negative')
        return v
    
    @validator('actual_hours')
    def validate_actual_hours(cls, v):
        if v is not None and v < 0:
            raise ValueError('Actual hours cannot be negative')
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            date: lambda v: v.isoformat()
        }
