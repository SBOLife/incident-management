"""
Database session module.

This module configures the SQLAlchemy engine and session factory for database operations.
It provides the core database connection functionality for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./incident-managment.db"
"""
The database connection URL.

This defines the location and type of the database. Currently configured to use SQLite
with a local file in the application root directory.
"""

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
"""
SQLAlchemy engine instance.

The engine is the starting point for any SQLAlchemy application. It maintains
a pool of connections to the database.

The 'check_same_thread' argument is set to False to allow SQLite to be used with
multiple threads, which is necessary for FastAPI's asynchronous operation.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
SQLAlchemy session factory.

This factory creates new database sessions that are used for database operations.
Configuration:
- autocommit=False: Changes must be explicitly committed
- autoflush=False: Changes won't be automatically flushed to the database
- bind=engine: Sessions are bound to the configured engine

Usage:
    db = SessionLocal()
    try:
        # Use the session for database operations
        result = db.query(Model).all()
        return result
    finally:
        db.close()  # Always close the session when done
"""