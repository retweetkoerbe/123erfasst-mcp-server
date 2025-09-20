"""
Project model for 123erfasst construction projects.

Follows Article VIII: Anti-Abstraction Principle - Single model representation for Project entity.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator


class Project(BaseModel):
    """
    Construction project entity.
    
    Represents a construction project with basic information and status.
    """
    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    status: Optional[str] = Field(None, description="Project status (active, completed, on_hold, cancelled)")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    description: Optional[str] = Field(None, description="Project description")
    client_name: Optional[str] = Field(None, description="Client name")
    budget: Optional[float] = Field(None, description="Project budget")
    location: Optional[str] = Field(None, description="Project location")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Project ID is required')
        return v.strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Project name is required')
        return v.strip()
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ['active', 'completed', 'on_hold', 'cancelled', 'planning']
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError('End date must be after start date')
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            date: lambda v: v.isoformat()
        }
