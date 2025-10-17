"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExampleBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: bool = True


class ExampleCreate(ExampleBase):
    """Schema for creating new example"""
    pass


class ExampleUpdate(BaseModel):
    """Schema for updating example (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None


class ExampleResponse(ExampleBase):
    """Schema for example response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Enable ORM mode


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    database: str
