"""
Database CRUD operations module.

This module provides Create, Read, Update, and Delete operations for the application's
database models, including incidents and users.
"""

from sqlalchemy.orm import Session
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentUpdate
from app.models.user import User
from app.core.security import hash_password

def create_incident(db: Session, incident: IncidentCreate):
    """
    Create a new incident in the database.
    
    Args:
        db (Session): The database session.
        incident (IncidentCreate): The incident data to create.
        
    Returns:
        Incident: The created incident object with database-populated fields.
    """
    db_incident = Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def get_incident(db: Session, incident_id: int = None, skip: int = 0, limit: int = 100):
    """
    Retrieve incident(s) from the database.
    
    If incident_id is provided, returns a single incident.
    Otherwise, returns a list of incidents with pagination.
    
    Args:
        db (Session): The database session.
        incident_id (int, optional): The ID of a specific incident to retrieve.
        skip (int, optional): Number of records to skip for pagination. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.
        
    Returns:
        Union[Incident, List[Incident]]: A single incident or list of incidents.
    """
    if incident_id:
        return db.query(Incident).filter(Incident.id == incident_id).first()
    return db.query(Incident).offset(skip).limit(limit).all()

def update_incident(db: Session, incident_id: int, incident: IncidentUpdate):
    """
    Update an existing incident in the database.
    
    Args:
        db (Session): The database session.
        incident_id (int): The ID of the incident to update.
        incident (IncidentUpdate): The updated incident data.
        
    Returns:
        Incident: The updated incident object.
    """
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    for key, value in incident.dict().items():
        setattr(db_incident, key, value)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def delete_incident(db: Session, incident_id: int):
    """
    Delete an incident from the database.
    
    Args:
        db (Session): The database session.
        incident_id (int): The ID of the incident to delete.
        
    Returns:
        Incident: The deleted incident object.
    """
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    db.delete(db_incident)
    db.commit()
    return db_incident

def get_user_by_username(db: Session, email: str) -> str:
    """
    Retrieve a user by their email address.
    
    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.
        
    Returns:
        User: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    """
    Create a new user in the database.
    
    This function hashes the provided password before storing it.
    
    Args:
        db (Session): The database session.
        email (str): The email address of the new user.
        password (str): The plain text password to be hashed and stored.
        
    Returns:
        User: The created user object.
    """
    hashed = hash_password(password)
    db_user = User(email=email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user