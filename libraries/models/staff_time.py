"""
StaffTime model for time tracking records.

Follows Article VIII: Anti-Abstraction Principle - Single model representation for StaffTime entity.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class StaffTime(BaseModel):
    """
    Time tracking record for staff members.
    
    Represents a time tracking entry for a person working on a project.
    """
    id: str = Field(..., description="Unique time tracking record identifier")
    project_id: str = Field(..., description="Project identifier")
    person_id: str = Field(..., description="Person identifier")
    start_time: Optional[datetime] = Field(None, description="Time tracking start time")
    end_time: Optional[datetime] = Field(None, description="Time tracking end time")
    duration_hours: Optional[float] = Field(None, description="Duration in hours")
    description: Optional[str] = Field(None, description="Work description")
    is_active: bool = Field(False, description="Whether time tracking is currently active")
    created_at: Optional[datetime] = Field(None, description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record last update timestamp")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('StaffTime ID is required')
        return v.strip()
    
    @validator('project_id')
    def validate_project_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Project ID is required')
        return v.strip()
    
    @validator('person_id')
    def validate_person_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Person ID is required')
        return v.strip()
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if v and 'start_time' in values and values['start_time']:
            if v <= values['start_time']:
                raise ValueError('End time must be after start time')
        return v
    
    @validator('duration_hours')
    def validate_duration_hours(cls, v, values):
        if v is not None and v < 0:
            raise ValueError('Duration hours cannot be negative')
        
        # Auto-calculate duration if start_time and end_time are provided
        if v is None and 'start_time' in values and 'end_time' in values:
            if values['start_time'] and values['end_time']:
                delta = values['end_time'] - values['start_time']
                return delta.total_seconds() / 3600  # Convert to hours
        
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
