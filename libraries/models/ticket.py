"""
Ticket model for quality management and issue tracking.

Follows Article VIII: Anti-Abstraction Principle - Single model representation for Ticket entity.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class Ticket(BaseModel):
    """
    Quality management ticket entity.
    
    Represents a ticket for tracking issues, defects, or quality concerns.
    """
    id: str = Field(..., description="Unique ticket identifier")
    title: str = Field(..., description="Ticket title")
    description: Optional[str] = Field(None, description="Detailed description")
    status: Optional[str] = Field(None, description="Ticket status (open, in_progress, resolved, closed)")
    priority: Optional[str] = Field(None, description="Priority level (low, medium, high, critical)")
    category: Optional[str] = Field(None, description="Ticket category (safety, quality, maintenance, other)")
    project_id: Optional[str] = Field(None, description="Related project ID")
    assigned_person_id: Optional[str] = Field(None, description="Assigned person ID")
    reporter_person_id: Optional[str] = Field(None, description="Person who reported the issue")
    created_at: Optional[datetime] = Field(None, description="Ticket creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    resolved_at: Optional[datetime] = Field(None, description="Resolution timestamp")
    location: Optional[str] = Field(None, description="Issue location")
    tags: Optional[list[str]] = Field(None, description="Tags for categorization")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Ticket ID is required')
        return v.strip()
    
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Ticket title is required')
        return v.strip()
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ['open', 'in_progress', 'resolved', 'closed', 'cancelled']
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None:
            valid_priorities = ['low', 'medium', 'high', 'critical']
            if v not in valid_priorities:
                raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return v
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            valid_categories = ['safety', 'quality', 'maintenance', 'equipment', 'other']
            if v not in valid_categories:
                raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
