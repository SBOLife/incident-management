
          
# Incident Management System

A comprehensive system for tracking, categorizing, and managing incidents.

## Overview

This incident management system provides a robust platform for organizations to track and manage incidents. It includes features for incident creation, automatic categorization, status tracking, and user authentication.

## Features

- **Incident Tracking**: Create, update, and monitor incidents
- **Automatic Classification**: Incidents are automatically categorized based on their description
- **User Authentication**: Secure JWT-based authentication system
- **RESTful API**: Well-documented API endpoints for integration

## Technical Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (configurable)
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **AI Classification**: Hugging Face Transformers with XLM-RoBERTa model

## Project Structure

```
incident-management/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── authentication.py  # Authentication endpoints
│   │   │   └── incidents.py       # Incident management endpoints
│   ├── core/
│   │   └── security.py            # Security utilities
│   ├── db/
│   │   ├── base.py                # SQLAlchemy base
│   │   ├── crud.py                # Database operations
│   │   └── session.py             # Database session management
│   ├── models/
│   │   ├── incident.py            # Incident database model
│   │   └── user.py                # User database model
│   ├── schemas/
│   │   ├── incident.py            # Incident Pydantic schemas
│   │   └── user.py                # User Pydantic schemas
│   └── services/
│       └── classifier.py          # Incident classification service
├── tests/
│   └── test_incident.py           # Tests for incident endpoints
├── main.py                        # Application entry point
├── init_db.py                     # Database initialization script
└── pyproject.toml                 # Project dependencies and configuration
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SBOLife/incident-management.git
   cd incident-management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- **POST /auth/token**: Authenticate and get JWT token
- **POST /incidents/**: Create a new incident
- **GET /incidents/**: List all incidents

## Authentication

The system uses JWT tokens for authentication. To access protected endpoints:

1. Obtain a token by sending a POST request to `/auth/token` with your credentials
2. Include the token in the Authorization header of subsequent requests:
   ```
   Authorization: Bearer your_token_here
   ```

## Incident Classification

Incidents are automatically classified using a pre-trained multilingual language model (XLM-RoBERTa) with zero-shot classification capabilities:

- The system uses natural language understanding to determine the most appropriate category
- No keyword matching is required
- the model understands the semantic meaning of the description
- Current categories include: Network Issue, Server Issue, Software Issue, Login Issue, and Others
- The classification model can be easily extended with additional categories

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Adding New Categories

To add new incident categories, modify the `classify_category` function in `app/services/classifier.py`.

## Hardware Requirements
- The classification model runs on CPU by default
- For improved performance, GPU acceleration can be enabled by changing the device parameter to "cuda"

## Dependencies
- Hugging Face Transformers library for the classification model
- The first run will download the pre-trained model (approximately 1.2GB)

## Security Considerations

- The default SECRET_KEY should be changed in production
- Database connection settings should be configured for your environment
- Consider implementing rate limiting for production deployments

## License

[APACHE 2.0](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Contact

For questions or support, please open an issue on the GitHub repository.
