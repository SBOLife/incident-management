"""
Incidents API module for the incident management system.
This module handles CRUD operations for incidents, including automatic classification.
"""

from fastapi import APIRouter, Depends, BackgroundTasks
from app.db.session import SessionLocal
from app.schemas.incident import IncidentCreate, IncidentUpdate, IncidentOut
from app.db.crud import create_incident, get_incident, update_incident
from app.services.classifier import classify_category
from app.api.endpoints.authentication import get_current_user

router = APIRouter()

def get_db():
    """
    Create and yield a database session.
    
    This dependency ensures proper database connection management by creating
    a new session for each request and closing it after the request is completed.
    
    Yields:
        SessionLocal: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/incidents/", response_model=IncidentOut)
def create(data: IncidentCreate, background_tasks: BackgroundTasks, db: SessionLocal = Depends(get_db), user: str = Depends(get_current_user)):
    """
    Create a new incident.
    
    This endpoint creates a new incident and schedules a background task to classify
    the incident based on its description.
    
    Args:
        data (IncidentCreate): The incident data to create.
        background_tasks (BackgroundTasks): FastAPI background tasks handler.
        db (SessionLocal): The database session dependency.
        user (str): The authenticated user dependency.
        
    Returns:
        IncidentOut: The created incident.
    """
    incident = create_incident(db, data)
    background_tasks.add_task(_classify, db, incident.id, incident.description)
    return incident

def _classify(db: SessionLocal, incident_id: int, description: str):
    """
    Classify an incident based on its description.
    
    This internal function is called as a background task to determine the category
    of an incident based on keywords in its description.
    
    Args:
        db (SessionLocal): The database session.
        incident_id (int): The ID of the incident to classify.
        description (str): The incident description text.
    """
    category = classify_category(description)
    update_incident(db, incident_id, IncidentUpdate(category=category))

@router.get("/", response_model=list[IncidentOut])
def list_all(db: SessionLocal = Depends(get_db), user: str = Depends(get_current_user)):
    """
    List all incidents.
    
    This endpoint retrieves all incidents from the database.
    Authentication is required to access this endpoint.
    
    Args:
        db (SessionLocal): The database session dependency.
        user (str): The authenticated user dependency.
        
    Returns:
        list[IncidentOut]: A list of all incidents.
    """
    return get_incident(db)