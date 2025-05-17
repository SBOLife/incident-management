"""
User model module.

This module defines the User database model for authentication and user management.
"""

from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    """
    User database model.
    
    This model represents a user in the incident management system.
    It stores essential user information for authentication and identification.
    """
    
    __tablename__ = "users"
    """Table name for the users model in the database."""

    id = Column(Integer, primary_key=True, index=True)
    """
    Primary key for the user record.
    
    This is an auto-incrementing integer that uniquely identifies each user.
    """
    
    email = Column(String, unique=True, index=True, nullable=False)
    """
    User's email address.
    
    Serves as the username for authentication purposes.
    Must be unique across all users and cannot be null.
    An index is created on this column to speed up lookups.
    """
    
    hashed_password = Column(String, nullable=False)
    """
    User's hashed password.
    
    Stores the bcrypt hash of the user's password, not the actual password.
    Cannot be null.
    """