"""
Performance Benchmark Configuration
"""
import pytest


def pytest_configure(config):
    """Configure pytest for benchmarking."""
    config.addinivalue_line(
        "markers", "benchmark: marks tests as performance benchmarks"
    )


@pytest.fixture(scope="session")
def benchmark_env():
    """Benchmark environment setup."""
    import os
    os.environ["APP_ENVIRONMENT"] = "benchmark"
    return {
        "warmup_iterations": 3,
        "min_rounds": 5,
        "max_time": 1.0
    }


@pytest.fixture(scope="function")
def benchmark_client():
    """Create a test client for benchmarking."""
    from fastapi.testclient import TestClient
    from src.api.main import app

    return TestClient(app)


@pytest.fixture(scope="function")
def benchmark_data():
    """Provide benchmark test data."""
    return {
        "test_text": "这是一个用于性能测试的文本示例",
        "test_memory": {
            "user_id": "benchmark_user",
            "content": "基准测试记忆内容",
            "type": "preference"
        },
        "test_intent": {
            "text": "查询天气",
            "context": {
                "user_id": "benchmark_user",
                "session_id": "benchmark_session"
            }
        }
    }
