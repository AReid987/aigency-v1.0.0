"""
Basic tests to validate the FastAPI backend setup
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.models.user import User
from app.auth.security import get_password_hash

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to" in response.json()["message"]

def test_api_docs_accessible():
    """Test that API documentation is accessible in development"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_user_registration():
    """Test user registration endpoint"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert response.json()["username"] == user_data["username"]

def test_user_login():
    """Test user login endpoint"""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpassword123",
        "full_name": "Login User"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Then try to login
    login_data = {
        "username": "login@example.com",
        "password": "loginpassword123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_sources_endpoint():
    """Test sources endpoint (requires authentication)"""
    # First get a token
    user_data = {
        "email": "sources@example.com",
        "username": "sourcesuser",
        "password": "sourcespassword123",
        "full_name": "Sources User"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    login_data = {
        "username": "sources@example.com",
        "password": "sourcespassword123"
    }
    login_response = client.post("/api/v1/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/sources/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_unauthorized_access():
    """Test that protected endpoints require authentication"""
    response = client.get("/api/v1/runs/")
    assert response.status_code == 401

def test_invalid_login():
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__, "-v"])