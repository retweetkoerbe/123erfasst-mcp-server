"""
Equipment model for construction equipment.

Follows Article VIII: Anti-Abstraction Principle - Single model representation for Equipment entity.
"""
from typing import Optional
from pydantic import BaseModel, Field, validator


class Equipment(BaseModel):
    """
    Construction equipment entity.
    
    Represents equipment used on construction projects.
    """
    id: str = Field(..., description="Unique equipment identifier")
    name: str = Field(..., description="Equipment name")
    type: Optional[str] = Field(None, description="Equipment type (e.g., Heavy Machinery, Tools)")
    location: Optional[str] = Field(None, description="Current location")
    status: Optional[str] = Field(None, description="Equipment status (operational, maintenance, out_of_service)")
    model: Optional[str] = Field(None, description="Equipment model")
    serial_number: Optional[str] = Field(None, description="Serial number")
    purchase_date: Optional[str] = Field(None, description="Purchase date")
    last_maintenance: Optional[str] = Field(None, description="Last maintenance date")
    next_maintenance: Optional[str] = Field(None, description="Next scheduled maintenance")
    assigned_project_id: Optional[str] = Field(None, description="Currently assigned project ID")
    assigned_person_id: Optional[str] = Field(None, description="Currently assigned person ID")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Equipment ID is required')
        return v.strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Equipment name is required')
        return v.strip()
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ['operational', 'maintenance', 'out_of_service', 'reserved']
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
