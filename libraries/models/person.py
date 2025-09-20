"""
Person model for staff members.

Follows Article VIII: Anti-Abstraction Principle - Single model representation for Person entity.
"""
from typing import Optional
from pydantic import BaseModel, Field, validator, EmailStr


class Person(BaseModel):
    """
    Staff member entity.
    
    Represents a person working on construction projects.
    """
    id: str = Field(..., description="Unique person identifier")
    name: str = Field(..., description="Person's full name")
    role: Optional[str] = Field(None, description="Job role or position")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    department: Optional[str] = Field(None, description="Department or team")
    is_active: bool = Field(True, description="Whether person is currently active")
    hire_date: Optional[str] = Field(None, description="Hire date")
    skills: Optional[list[str]] = Field(None, description="List of skills or certifications")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Person ID is required')
        return v.strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Person name is required')
        return v.strip()
    
    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            # Basic phone validation - remove common separators and + sign
            cleaned = v.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', '')
            if not cleaned.isdigit() or len(cleaned) < 10:
                raise ValueError('Phone number must contain at least 10 digits')
        return v
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
