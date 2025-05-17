"""
User schema module.

This module defines Pydantic models for user data validation, serialization, and deserialization.
These schemas are used for API request/response handling and user management operations.
"""

from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Schema for user creation.
    
    This schema is used for validating data when creating a new user.
    It contains the essential fields required for user registration.
    """
    email: str
    """
    User's email address.
    
    This serves as the username for authentication purposes and must be unique.
    """
    
    password: str
    """
    User's plain text password.
    
    This field is used only during user creation. The password is hashed
    before storage and the plain text version is never stored in the database.
    """