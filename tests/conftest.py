"""
Pytest Configuration and Fixtures
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Test configuration
TEST_API_URL = "http://localhost:8000"
TEST_DB_URL = "postgresql://test:test@localhost:5432/xuanji_engine_test"
TEST_REDIS_URL = "redis://localhost:6379/1"

# Synchronous engine for tests
test_engine = create_engine(TEST_DB_URL, pool_pre_ping=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a new database session for a test."""
    session = TestSessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()

@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing API endpoints."""
    async with AsyncClient(base_url=TEST_API_URL) as client:
        yield client

@pytest.fixture(scope="function")
def auth_token(db_session: Session) -> str:
    """Create a test authentication token."""
    # Create test user
    # Return test token
    return "test_token_12345"

@pytest.fixture(scope="function")
def test_user_data() -> dict:
    """Return test user data."""
    return {
        "user_id": "test_user_123",
        "username": "test_user",
        "email": "test@example.com"
    }

@pytest.fixture(scope="function")
def test_memory_data() -> dict:
    """Return test memory data."""
    return {
        "user_id": "test_user_123",
        "content": "测试记忆内容",
        "type": "preference",
        "timestamp": "2026-03-18T22:00:00Z"
    }

@pytest.fixture(scope="function")
def test_intent_data() -> dict:
    """Return test intent recognition data."""
    return {
        "text": "帮我查询一下明天的天气",
        "context": {
            "user_id": "test_user_123",
            "session_id": "test_session_456"
        }
    }

@pytest.fixture(scope="function")
def test_dialogue_data() -> dict:
    """Return test dialogue data."""
    return {
        "message": "你好",
        "user_id": "test_user_123",
        "session_id": "test_session_456"
    }

# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
