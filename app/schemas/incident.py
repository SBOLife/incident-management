"""
Incident schema module.

This module defines Pydantic models for incident data validation, serialization, and deserialization.
These schemas are used for API request/response handling and data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentBase(BaseModel):
    """
    Base Incident schema with common attributes.
    
    This class contains the common attributes shared by all incident-related schemas.
    It serves as the foundation for other incident schemas.
    """
    title: str
    """Title of the incident. Required string field."""
    
    description: str
    """Detailed description of the incident. Required string field."""

class IncidentCreate(IncidentBase):
    """
    Schema for incident creation.
    
    This schema is used for validating data when creating a new incident.
    It inherits all fields from IncidentBase.
    """
    pass

class IncidentUpdate(BaseModel):
    """
    Schema for incident updates.
    
    This schema is used for validating data when updating an existing incident.
    It contains only the fields that can be updated.
    """
    status: str = "new"
    """
    Current status of the incident.
    
    Defaults to "new" if not provided during update.
    """
    
    category: Optional[str]
    """
    Category of the incident.
    
    Optional field that can be null/None.
    """

class IncidentOut(IncidentBase):
    """
    Schema for incident responses.
    
    This schema is used for serializing incident data in API responses.
    It includes all incident fields, including database-generated ones.
    """
    id: int
    """Unique identifier for the incident."""
    
    created_at: datetime
    """Timestamp when the incident was created."""
    
    updated_at: datetime
    """Timestamp when the incident was last updated."""
    
    status: str
    """Current status of the incident."""
    
    category: Optional[str]
    """Category of the incident. Can be null/None."""

    class Config:
        """Pydantic configuration for the schema."""
        from_attributes = True  # Updated from orm_mode = True
        """
        Enables ORM mode (renamed to from_attributes in Pydantic v2).
        
        This allows the model to read data from SQLAlchemy ORM models.
        """