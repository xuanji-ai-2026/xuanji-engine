"""
Data Tests
"""
import pytest
from sqlalchemy.orm import Session
from tests.conftest import TestSessionLocal


class TestMemoryStorage:
    """Memory storage tests."""

    @pytest.mark.unit
    def test_store_memory(self, db_session: Session, test_memory_data: dict):
        """Test storing memory to database."""
        # Import memory storage module
        from src.jumen.memory_storage_shen import MemoryStorage

        storage = MemoryStorage()
        result = storage.store(db_session, test_memory_data)

        assert result is not None
        assert "memory_id" in result
        assert isinstance(result["memory_id"], str)

    @pytest.mark.unit
    def test_retrieve_memory(self, db_session: Session, test_memory_data: dict):
        """Test retrieving memory from database."""
        from src.jumen.memory_storage_shen import MemoryStorage
        from src.jumen.memory_retrieve_han import MemoryRetrieve

        # First store the memory
        storage = MemoryStorage()
        store_result = storage.store(db_session, test_memory_data)
        memory_id = store_result["memory_id"]

        # Then retrieve it
        retrieve = MemoryRetrieve()
        result = retrieve.retrieve(db_session, memory_id)

        assert result is not None
        assert result["content"] == test_memory_data["content"]
        assert result["type"] == test_memory_data["type"]

    @pytest.mark.unit
    def test_memory_consistency(self, db_session: Session, test_memory_data: dict):
        """Test memory data consistency."""
        from src.jumen.memory_storage_shen import MemoryStorage
        from src.jumen.memory_retrieve_han import MemoryRetrieve

        storage = MemoryStorage()
        retrieve = MemoryRetrieve()

        # Store memory
        store_result = storage.store(db_session, test_memory_data)
        memory_id = store_result["memory_id"]

        # Retrieve and verify
        result = retrieve.retrieve(db_session, memory_id)
        assert result is not None
        assert result["user_id"] == test_memory_data["user_id"]
        assert result["content"] == test_memory_data["content"]
        assert result["type"] == test_memory_data["type"]


class TestMemoryIndexing:
    """Memory indexing tests."""

    @pytest.mark.unit
    def test_create_index(self, db_session: Session, test_memory_data: dict):
        """Test creating memory index."""
        from src.jumen.memory_index_yang import MemoryIndex

        index = MemoryIndex()
        # First store memory
        from src.jumen.memory_storage_shen import MemoryStorage
        storage = MemoryStorage()
        store_result = storage.store(db_session, test_memory_data)
        memory_id = store_result["memory_id"]

        # Create index
        result = index.create(db_session, memory_id, test_memory_data["content"])

        assert result is not None
        assert "index_id" in result

    @pytest.mark.unit
    def test_search_by_index(self, db_session: Session, test_memory_data: dict):
        """Test searching memory by index."""
        from src.jumen.memory_storage_shen import MemoryStorage
        from src.jumen.memory_index_yang import MemoryIndex

        storage = MemoryStorage()
        index = MemoryIndex()

        # Store memory and create index
        store_result = storage.store(db_session, test_memory_data)
        memory_id = store_result["memory_id"]
        index.create(db_session, memory_id, test_memory_data["content"])

        # Search
        result = index.search(db_session, "测试记忆")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0


class TestDataIntegrity:
    """Data integrity tests."""

    @pytest.mark.unit
    def test_user_data_isolation(self, db_session: Session):
        """Test user data isolation."""
        from src.jumen.memory_storage_shen import MemoryStorage

        storage = MemoryStorage()

        # Store memories for different users
        user1_memory = {
            "user_id": "user1",
            "content": "User1的记忆",
            "type": "preference"
        }

        user2_memory = {
            "user_id": "user2",
            "content": "User2的记忆",
            "type": "preference"
        }

        result1 = storage.store(db_session, user1_memory)
        result2 = storage.store(db_session, user2_memory)

        assert result1["memory_id"] != result2["memory_id"]
        assert result1["user_id"] == "user1"
        assert result2["user_id"] == "user2"

    @pytest.mark.unit
    def test_data_validation(self, db_session: Session):
        """Test data validation."""
        from src.jumen.memory_storage_shen import MemoryStorage

        storage = MemoryStorage()

        # Test invalid data
        invalid_memory = {
            "user_id": "",  # Empty user_id
            "content": "",  # Empty content
            "type": "invalid_type"  # Invalid type
        }

        result = storage.store(db_session, invalid_memory)

        assert result is None or "error" in result


class TestRedisCache:
    """Redis cache tests."""

    @pytest.mark.unit
    def test_cache_set_get(self):
        """Test setting and getting cache."""
        import redis

        r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

        # Set cache
        r.set("test_key", "test_value", ex=60)

        # Get cache
        value = r.get("test_key")

        assert value == "test_value"

        # Cleanup
        r.delete("test_key")

    @pytest.mark.unit
    def test_cache_expiration(self):
        """Test cache expiration."""
        import redis
        import time

        r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

        # Set cache with short expiration
        r.set("expire_test", "test_value", ex=1)

        # Should exist immediately
        assert r.get("expire_test") is not None

        # Wait for expiration
        time.sleep(2)

        # Should be expired
        assert r.get("expire_test") is None


class TestDatabaseConnection:
    """Database connection tests."""

    @pytest.mark.unit
    def test_db_connection(self):
        """Test database connection."""
        from tests.conftest import test_engine

        connection = test_engine.connect()
        result = connection.execute("SELECT 1")
        assert result.scalar() == 1
        connection.close()

    @pytest.mark.unit
    def test_db_session_pool(self):
        """Test database session pool."""
        from tests.conftest import TestSessionLocal

        sessions = []
        for _ in range(5):
            session = TestSessionLocal()
            sessions.append(session)
            connection = session.connection()
            assert connection is not None

        # Cleanup
        for session in sessions:
            session.close()
