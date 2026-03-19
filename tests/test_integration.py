"""
Integration Tests
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session


class TestE2EDialogueFlow:
    """End-to-end dialogue flow tests."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complete_dialogue_flow(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_user_data: dict
    ):
        """Test complete dialogue flow from login to conversation."""
        # Step 1: Login
        login_response = await async_client.post(
            "/api/v2/auth/login",
            json={
                "username": test_user_data["username"],
                "password": "test_password"
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        token = login_data["data"]["token"]

        # Step 2: Send greeting message
        greeting_response = await async_client.post(
            "/api/v2/dialogue/message",
            json={
                "message": "你好",
                "user_id": test_user_data["user_id"],
                "session_id": "test_session_integration"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert greeting_response.status_code == 200
        greeting_data = greeting_response.json()
        assert "reply" in greeting_data["data"]

        # Step 3: Recognize intent
        intent_response = await async_client.post(
            "/api/v2/intent/recognize",
            json={
                "text": "帮我查询一下天气",
                "context": {
                    "user_id": test_user_data["user_id"],
                    "session_id": "test_session_integration"
                }
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert intent_response.status_code == 200
        intent_data = intent_response.json()
        assert "intent" in intent_data["data"]

        # Step 4: Store memory
        memory_response = await async_client.post(
            "/api/v2/memory/store",
            json={
                "user_id": test_user_data["user_id"],
                "content": "用户喜欢查询天气",
                "type": "preference",
                "timestamp": "2026-03-18T22:00:00Z"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert memory_response.status_code == 200
        memory_data = memory_response.json()
        assert "memory_id" in memory_data["data"]


class TestServiceCommunication:
    """Service-to-service communication tests."""

    @pytest.mark.integration
    def test_intent_to_dialogue_flow(self, db_session: Session, test_intent_data: dict):
        """Test flow from intent recognition to dialogue management."""
        from src.ziwei.intent_recognition import IntentRecognition
        from src.tanlang.dialog_manage_lei import DialogueManager

        # Recognize intent
        recognizer = IntentRecognition()
        intent_result = recognizer.recognize(test_intent_data["text"])

        assert intent_result is not None
        assert "intent" in intent_result

        # Generate dialogue response
        dialogue_manager = DialogueManager()
        dialogue_response = dialogue_manager.generate_response(
            intent=intent_result["intent"],
            user_id=test_intent_data["context"]["user_id"]
        )

        assert dialogue_response is not None
        assert "reply" in dialogue_response

    @pytest.mark.integration
    def test_memory_to_intent_flow(self, db_session: Session, test_memory_data: dict):
        """Test flow from memory storage to intent recognition."""
        from src.jumen.memory_storage_shen import MemoryStorage
        from src.jumen.memory_retrieve_han import MemoryRetrieve
        from src.ziwei.intent_recognition import IntentRecognition

        # Store memory
        storage = MemoryStorage()
        store_result = storage.store(db_session, test_memory_data)
        memory_id = store_result["memory_id"]

        # Retrieve memory
        retrieve = MemoryRetrieve()
        memory_result = retrieve.retrieve(db_session, memory_id)

        assert memory_result is not None

        # Use memory for intent recognition
        recognizer = IntentRecognition()
        # This would use the stored memory to improve intent recognition
        intent_result = recognizer.recognize_with_context(
            text="我想要上次提到的",
            context={
                "user_id": test_memory_data["user_id"],
                "recent_memories": [memory_result]
            }
        )

        assert intent_result is not None


class TestConcurrentRequests:
    """Concurrent request handling tests."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_dialogue_requests(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_user_data: dict
    ):
        """Test handling multiple concurrent dialogue requests."""
        import asyncio

        async def send_message(message: str):
            response = await async_client.post(
                "/api/v2/dialogue/message",
                json={
                    "message": message,
                    "user_id": test_user_data["user_id"],
                    "session_id": "test_session_concurrent"
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            return response

        # Send 10 concurrent requests
        messages = ["你好"] * 10
        responses = await asyncio.gather(*[send_message(msg) for msg in messages])

        # All requests should succeed
        assert len(responses) == 10
        assert all(r.status_code == 200 for r in responses)


class TestErrorRecovery:
    """Error recovery tests."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_service_failure_recovery(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_intent_data: dict
    ):
        """Test system recovery from service failure."""
        # Simulate service failure by sending invalid data
        invalid_data = {"invalid": "data"}

        response = await async_client.post(
            "/api/v2/intent/recognize",
            json=invalid_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Should return error without crashing
        assert response.status_code in [400, 500]

        # System should still work for valid requests
        valid_response = await async_client.post(
            "/api/v2/intent/recognize",
            json=test_intent_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert valid_response.status_code == 200


class TestPerformanceUnderLoad:
    """Performance tests under load."""

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_performance_under_load(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_user_data: dict
    ):
        """Test system performance under load."""
        import asyncio
        import time

        start_time = time.time()

        # Send 100 requests
        async def send_request(i: int):
            response = await async_client.post(
                "/api/v2/dialogue/message",
                json={
                    "message": f"测试消息{i}",
                    "user_id": test_user_data["user_id"],
                    "session_id": f"test_session_{i}"
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            return response

        responses = await asyncio.gather(*[send_request(i) for i in range(100)])

        end_time = time.time()
        total_time = end_time - start_time

        # All requests should succeed
        assert len(responses) == 100
        assert all(r.status_code == 200 for r in responses)

        # Should complete in reasonable time (< 30 seconds for 100 requests)
        assert total_time < 30

        # Average response time should be < 300ms
        avg_time = total_time / 100
        assert avg_time < 0.3


class TestDataConsistency:
    """Data consistency tests."""

    @pytest.mark.integration
    def test_cross_service_data_consistency(self, db_session: Session, test_memory_data: dict):
        """Test data consistency across services."""
        from src.jumen.memory_storage_shen import MemoryStorage
        from src.jumen.memory_retrieve_han import MemoryRetrieve
        from src.jumen.memory_index_yang import MemoryIndex

        storage = MemoryStorage()
        retrieve = MemoryRetrieve()
        index = MemoryIndex()

        # Store memory
        store_result = storage.store(db_session, test_memory_data)
        memory_id = store_result["memory_id"]

        # Create index
        index_result = index.create(db_session, memory_id, test_memory_data["content"])

        # Retrieve and verify consistency
        retrieve_result = retrieve.retrieve(db_session, memory_id)

        assert retrieve_result["content"] == test_memory_data["content"]
        assert retrieve_result["type"] == test_memory_data["type"]
        assert retrieve_result["user_id"] == test_memory_data["user_id"]
