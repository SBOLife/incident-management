"""
Authentication module for the incident management system.
This module handles user authentication, token generation, and validation.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

db = SessionLocal()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """
    Create a new JWT access token.
    
    Args:
        data (dict): The data to encode in the token, typically contains user information.
        
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and provide an access token.
    
    This endpoint is used for user login. It validates the provided credentials
    and returns a JWT token if authentication is successful.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username (email) and password.
        
    Returns:
        dict: A dictionary containing the access token and token type.
        
    Raises:
        HTTPException: If the credentials are invalid.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current authenticated user from the provided token.
    
    This function is used as a dependency in protected endpoints to validate
    the JWT token and retrieve the corresponding user.
    
    Args:
        token (str): The JWT token from the Authorization header.
        
    Returns:
        User: The authenticated user object.
        
    Raises:
        HTTPException: If the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user