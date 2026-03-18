"""
API Tests
"""
import pytest
from httpx import AsyncClient
from tests.conftest import TEST_API_URL


class TestHealthCheck:
    """Health check API tests."""

    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_client: AsyncClient):
        """Test health check endpoint."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_ready_endpoint(self, async_client: AsyncClient):
        """Test readiness check endpoint."""
        response = await async_client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestAuthentication:
    """Authentication API tests."""

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, test_user_data: dict):
        """Test successful login."""
        response = await async_client.post(
            "/api/v2/auth/login",
            json={
                "username": test_user_data["username"],
                "password": "test_password"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["code"] == 200
        assert "data" in data
        assert "token" in data["data"]

    @pytest.mark.asyncio
    async def test_login_failure(self, async_client: AsyncClient):
        """Test failed login with wrong credentials."""
        response = await async_client.post(
            "/api/v2/auth/login",
            json={
                "username": "wrong_user",
                "password": "wrong_password"
            }
        )
        assert response.status_code in [400, 401]


class TestIntentRecognition:
    """Intent recognition API tests."""

    @pytest.mark.asyncio
    async def test_intent_recognize(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_intent_data: dict
    ):
        """Test intent recognition endpoint."""
        response = await async_client.post(
            "/api/v2/intent/recognize",
            json=test_intent_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["code"] == 200
        assert "data" in data
        assert "intent" in data["data"]
        assert "confidence" in data["data"]

    @pytest.mark.asyncio
    async def test_intent_recognize_unauthorized(self, async_client: AsyncClient, test_intent_data: dict):
        """Test intent recognition without authorization."""
        response = await async_client.post(
            "/api/v2/intent/recognize",
            json=test_intent_data
        )
        assert response.status_code == 401


class TestDialogueManagement:
    """Dialogue management API tests."""

    @pytest.mark.asyncio
    async def test_send_message(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_dialogue_data: dict
    ):
        """Test send message endpoint."""
        response = await async_client.post(
            "/api/v2/dialogue/message",
            json=test_dialogue_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["code"] == 200
        assert "data" in data
        assert "reply" in data["data"]


class TestMemoryStorage:
    """Memory storage API tests."""

    @pytest.mark.asyncio
    async def test_store_memory(
        self,
        async_client: AsyncClient,
        auth_token: str,
        test_memory_data: dict
    ):
        """Test store memory endpoint."""
        response = await async_client.post(
            "/api/v2/memory/store",
            json=test_memory_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["code"] == 200
        assert "data" in data
        assert "memory_id" in data["data"]


class TestPersonality:
    """Personality API tests."""

    @pytest.mark.asyncio
    async def test_get_personality(self, async_client: AsyncClient, auth_token: str, test_user_data: dict):
        """Test get personality endpoint."""
        response = await async_client.get(
            f"/api/v2/personality/{test_user_data['user_id']}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["code"] == 200
        assert "data" in data
        assert "personality" in data["data"]


class TestErrorHandling:
    """Error handling tests."""

    @pytest.mark.asyncio
    async def test_404_not_found(self, async_client: AsyncClient, auth_token: str):
        """Test 404 error handling."""
        response = await async_client.get(
            "/api/v2/invalid-endpoint",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_400_bad_request(self, async_client: AsyncClient, auth_token: str):
        """Test 400 error handling."""
        response = await async_client.post(
            "/api/v2/intent/recognize",
            json={},  # Empty request
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_429_rate_limit(self, async_client: AsyncClient, auth_token: str):
        """Test rate limiting."""
        # Send multiple requests quickly
        responses = []
        for _ in range(100):
            response = await async_client.get(
                "/health",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            responses.append(response)
            if response.status_code == 429:
                break
        # At least one should be rate limited
        assert any(r.status_code == 429 for r in responses)
