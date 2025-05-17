"""
Database base module.

This module provides the declarative base class for all models in the application.
The Base class is used for creating SQLAlchemy ORM models that map to database tables.
"""

from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()
"""
Base class for all ORM models.

This class serves as the base for all SQLAlchemy ORM models in the application.
All model classes should inherit from this Base class to be properly mapped
to database tables and managed by SQLAlchemy's ORM system.

Example:
    ```python
    from app.db.base import Base
    
    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String)
    ```
"""