"""
Benchmark Tests
"""
import pytest


@pytest.mark.benchmark
def test_intent_recognition_speed(benchmark):
    """Benchmark intent recognition speed."""
    from src.ziwei.intent_recognition import IntentRecognition

    recognizer = IntentRecognition()

    def recognize_intent():
        return recognizer.recognize("帮我查询一下天气")

    result = benchmark(recognize_intent)

    assert result is not None
    assert "intent" in result


@pytest.mark.benchmark
def test_memory_storage_speed(benchmark):
    """Benchmark memory storage speed."""
    from src.jumen.memory_storage_shen import MemoryStorage

    storage = MemoryStorage()

    test_memory = {
        "user_id": "test_user",
        "content": "测试记忆内容",
        "type": "preference"
    }

    def store_memory():
        return storage.store(None, test_memory)  # Pass None for session

    result = benchmark(store_memory)

    assert result is not None


@pytest.mark.benchmark
def test_memory_retrieval_speed(benchmark):
    """Benchmark memory retrieval speed."""
    from src.jumen.memory_retrieve_han import MemoryRetrieve

    retrieve = MemoryRetrieve()

    memory_id = "test_memory_id"

    def retrieve_memory():
        return retrieve.retrieve(None, memory_id)  # Pass None for session

    result = benchmark(retrieve_memory)

    # May return None if memory doesn't exist, which is fine for benchmark


@pytest.mark.benchmark
def test_dialogue_generation_speed(benchmark):
    """Benchmark dialogue generation speed."""
    from src.tanlang.dialog_manage_lei import DialogueManager

    dialogue_manager = DialogueManager()

    def generate_response():
        return dialogue_manager.generate_response(
            intent="weather_query",
            user_id="test_user"
        )

    result = benchmark(generate_response)

    assert result is not None
    assert "reply" in result


@pytest.mark.benchmark
def test_api_health_check_speed(benchmark, benchmark_client):
    """Benchmark API health check speed."""
    def check_health():
        return benchmark_client.get("/health")

    response = benchmark(check_health)

    assert response.status_code == 200


@pytest.mark.benchmark
def test_api_intent_endpoint_speed(benchmark, benchmark_client, test_user_data):
    """Benchmark API intent recognition endpoint speed."""
    benchmark_client.post(
        "/api/v2/auth/login",
        json={
            "username": test_user_data["username"],
            "password": "test_password"
        }
    )

    test_intent = {
        "text": "查询天气",
        "context": {
            "user_id": test_user_data["user_id"],
            "session_id": "test_session"
        }
    }

    def call_intent_api():
        return benchmark_client.post(
            "/api/v2/intent/recognize",
            json=test_intent
        )

    response = benchmark(call_intent_api)

    assert response.status_code == 200


@pytest.mark.benchmark
def test_redis_cache_speed(benchmark):
    """Benchmark Redis cache operations."""
    import redis

    r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

    # Test SET
    def cache_set():
        r.set("bench_key", "bench_value")
        r.get("bench_key")

    benchmark(cache_set)

    # Cleanup
    r.delete("bench_key")


@pytest.mark.benchmark
def test_database_query_speed(benchmark):
    """Benchmark database query speed."""
    from sqlalchemy import create_engine
    from tests.conftest import TEST_DB_URL

    engine = create_engine(TEST_DB_URL, pool_pre_ping=True)

    def execute_query():
        with engine.connect() as conn:
            return conn.execute("SELECT 1").scalar()

    result = benchmark(execute_query)

    assert result == 1

    engine.dispose()


@pytest.mark.benchmark
def test_concurrent_task_execution_speed(benchmark):
    """Benchmark concurrent task execution."""
    import asyncio
    from src.pohjun.task_execute_yun import TaskExecutor

    executor = TaskExecutor()

    def execute_tasks():
        tasks = [
            {"id": i, "task": f"test_task_{i}"}
            for i in range(10)
        ]
        return asyncio.run(executor.execute_batch(tasks))

    results = benchmark(execute_tasks)

    assert len(results) == 10

    executor.cleanup()


@pytest.mark.benchmark
def test_plugin_loading_speed(benchmark):
    """Benchmark plugin loading speed."""
    from src.wuqu.plugin_system import PluginSystem

    plugin_system = PluginSystem()

    def load_plugins():
        return plugin_system.load_all()

    benchmark(load_plugins)

    plugin_system.cleanup()
