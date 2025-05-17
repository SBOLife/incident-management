"""
Incident model module.

This module defines the Incident database model for storing and managing incident records.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class Incident(Base):
    """
    Incident database model.
    
    This model represents an incident in the incident management system.
    It stores information about incidents including their title, description,
    status, category, and timestamps.
    """
    
    __tablename__ = "incidents"
    """Table name for the incidents model in the database."""

    id = Column(Integer, primary_key=True, index=True)
    """
    Primary key for the incident record.
    
    This is an auto-incrementing integer that uniquely identifies each incident.
    """
    
    title = Column(String, nullable=False)
    """
    Title of the incident.
    
    A short, descriptive name for the incident. Cannot be null.
    """
    
    description = Column(String, nullable=False)
    """
    Detailed description of the incident.
    
    Contains the full details of what happened, steps to reproduce, etc. Cannot be null.
    """
    
    status = Column(String, default="open")
    """
    Current status of the incident.
    
    Tracks the incident's current state (e.g., "open", "in progress", "resolved").
    Defaults to "open" when a new incident is created.
    """
    
    category = Column(String, nullable=True)
    """
    Category of the incident.
    
    Classifies the incident by type (e.g., "Network Issue", "Server Issue").
    This field is optional and can be automatically classified by the system.
    """
    
    created_at = Column(DateTime, default=datetime.utcnow)
    """
    Timestamp when the incident was created.
    
    Automatically set to the current UTC time when the incident is first created.
    """
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    """
    Timestamp when the incident was last updated.
    
    Automatically set to the current UTC time when the incident is created or updated.
    """