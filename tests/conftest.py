"""
Pytest configuration and fixtures
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql import func

# Set testing environment
os.environ["TESTING"] = "1"
os.environ["DB_SCHEMA"] = ""  # Disable schema for SQLite

from app.main import app
from app.database import get_db


# Create in-memory SQLite database for testing (without schema)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base without schema for testing
metadata = MetaData()
TestBase = declarative_base(metadata=metadata)


# Re-define models without schema for SQLite
class ExampleModel(TestBase):
    """Test version of ExampleModel without schema"""
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000))
    value = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    TestBase.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        TestBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Skip startup event that tries to initialize PostgreSQL
    app.router.on_startup = []
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
