"""
Test module for incident endpoints.

This module contains tests for the incident API endpoints, including
creation, listing, and classification functionality.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.db.crud import create_incident, get_incident, update_incident
from app.schemas.incident import IncidentCreate, IncidentUpdate
from app.models.incident import Incident
from datetime import datetime

client = TestClient(app)

# Mock user for authentication
@pytest.fixture
def mock_current_user():
    return {"id": 1, "email": "test@example.com"}

# Mock the get_current_user dependency
@pytest.fixture
def auth_headers(mock_current_user):
    return {"Authorization": "Bearer fake_token"}

# Mock database session
@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

# Sample incident data
@pytest.fixture
def sample_incident_data():
    return {
        "title": "Test Incident",
        "description": "This is a test network incident"
    }

# Sample incident object
@pytest.fixture
def sample_incident():
    return Incident(
        id=1,
        title="Test Incident",
        description="This is a test network incident",
        status="new",
        category="Network Issue",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

# Test creating an incident
@patch("app.api.endpoints.incidents.get_current_user")
@patch("app.api.endpoints.incidents.get_db")
def test_create_incident(mock_get_db, mock_get_current_user, mock_db, mock_current_user, sample_incident_data, sample_incident):
    # Setup mocks
    mock_get_current_user.return_value = mock_current_user
    mock_get_db.return_value = mock_db
    
    # Mock the create_incident function
    with patch("app.api.endpoints.incidents.create_incident") as mock_create:
        mock_create.return_value = sample_incident
        
        # Make the request
        response = client.post("/incidents/", json=sample_incident_data)
        
        # Assert response
        assert response.status_code == 200
        assert response.json()["title"] == sample_incident_data["title"]
        assert response.json()["description"] == sample_incident_data["description"]
        assert "id" in response.json()
        
        # Verify create_incident was called with correct data
        mock_create.assert_called_once()
        
        # Verify background task was added
        # Note: This is challenging to test directly, but we can check the function was imported

# Test listing all incidents
@patch("app.api.endpoints.incidents.get_current_user")
@patch("app.api.endpoints.incidents.get_db")
def test_list_all_incidents(mock_get_db, mock_get_current_user, mock_db, mock_current_user, sample_incident):
    # Setup mocks
    mock_get_current_user.return_value = mock_current_user
    mock_get_db.return_value = mock_db
    
    # Mock the get_incident function
    with patch("app.api.endpoints.incidents.get_incident") as mock_get:
        mock_get.return_value = [sample_incident]
        
        # Make the request
        response = client.get("/")
        
        # Assert response
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0]["title"] == sample_incident.title
        assert response.json()[0]["description"] == sample_incident.description
        
        # Verify get_incident was called
        mock_get.assert_called_once_with(mock_db)

# Test the classification function
def test_classify_incident():
    from app.services.classifier import classify_category
    
    # Test network classification
    assert classify_category("Network is down") == "Network Issue"
    
    # Test server classification
    assert classify_category("Server not responding") == "Server Issue"
    
    # Test software classification
    assert classify_category("Software bug found") == "Software Issue"
    
    # Test login classification
    assert classify_category("Cannot login to system") == "Login Issue"
    
    # Test default classification
    assert classify_category("Unknown problem") == "Other"

# Test the background classification task
@patch("app.api.endpoints.incidents.update_incident")
def test_classify_background_task(mock_update):
    from app.api.endpoints.incidents import _classify
    
    # Create mock db and incident
    mock_db = MagicMock()
    incident_id = 1
    description = "Network is down"
    
    # Call the function
    _classify(mock_db, incident_id, description)
    
    # Verify update_incident was called with correct parameters
    mock_update.assert_called_once()
    args, kwargs = mock_update.call_args
    assert args[0] == mock_db
    assert args[1] == incident_id
    assert isinstance(args[2], IncidentUpdate)
    assert args[2].category == "Network Issue"