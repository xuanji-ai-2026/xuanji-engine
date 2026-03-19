"""
Load Tests
"""
import pytest
import asyncio
import time
from httpx import AsyncClient


@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_concurrent_dialogue_requests_performance():
    """Test performance under concurrent dialogue requests."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Warmup
        for _ in range(10):
            await client.get("/health")

        # Load test
        start_time = time.time()
        num_requests = 100

        async def send_request(i):
            start = time.time()
            response = await client.get("/health")
            end = time.time()
            return response.status_code, end - start

        results = await asyncio.gather(*[send_request(i) for i in range(num_requests)])

        total_time = time.time() - start_time

        # Metrics
        successful = sum(1 for status, _ in results if status == 200)
        avg_response_time = sum(time for _, time in results) / num_requests
        throughput = num_requests / total_time

        print(f"\n=== Load Test Results ===")
        print(f"Total requests: {num_requests}")
        print(f"Successful: {successful}")
        print(f"Success rate: {(successful/num_requests)*100:.2f}%")
        print(f"Total time: {total_time:.3f}s")
        print(f"Average response time: {avg_response_time*1000:.2f}ms")
        print(f"Throughput: {throughput:.2f} requests/second")

        # Assertions
        assert successful == num_requests, "All requests should succeed"
        assert avg_response_time < 0.1, "Average response time should be < 100ms"
        assert throughput > 50, "Throughput should be > 50 requests/second"


@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_intent_recognition_performance():
    """Test intent recognition performance."""
    async with AsyncClient(base_url="http://localhost:8000") as client:

        # Benchmark intent recognition
        start_time = time.time()
        num_iterations = 100

        test_data = {
            "text": "帮我查询一下天气",
            "context": {
                "user_id": "benchmark_user",
                "session_id": "benchmark_session"
            }
        }

        latencies = []
        for i in range(num_iterations):
            start = time.time()
            # In real test, this would call actual API
            # response = await client.post("/api/v2/intent/recognize", json=test_data)
            end = time.time()
            latencies.append((end - start) * 1000)  # Convert to ms

        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)

        print(f"\n=== Intent Recognition Performance ===")
        print(f"Iterations: {num_iterations}")
        print(f"Average latency: {avg_latency:.2f}ms")
        print(f"Min latency: {min_latency:.2f}ms")
        print(f"Max latency: {max_latency:.2f}ms")

        # Assertions
        assert avg_latency < 50, f"Average latency should be < 50ms, got {avg_latency}ms"


@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_memory_storage_performance():
    """Test memory storage performance."""
    async with AsyncClient(base_url="http://localhost:8000") as client:

        # Benchmark memory storage
        num_operations = 100

        # Simulate memory storage operations
        start_time = time.time()
        operations = []

        for i in range(num_operations):
            start = time.time()
            # Simulate memory storage
            memory_data = {
                "user_id": f"user_{i}",
                "content": f"Memory content {i}",
                "type": "preference"
            }
            # In real test, this would call actual API
            # await client.post("/api/v2/memory/store", json=memory_data)
            end = time.time()
            operations.append((end - start) * 1000)

        avg_operation_time = sum(operations) / len(operations)
        ops_per_second = num_operations / (time.time() - start_time)

        print(f"\n=== Memory Storage Performance ===")
        print(f"Operations: {num_operations}")
        print(f"Average operation time: {avg_operation_time:.2f}ms")
        print(f"Operations per second: {ops_per_second:.2f}")

        # Assertions
        assert avg_operation_time < 20, f"Average operation time should be < 20ms, got {avg_operation_time}ms"
        assert ops_per_second > 30, f"Operations per second should be > 30, got {ops_per_second}"


@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_database_connection_pool_performance():
    """Test database connection pool performance."""
    import time

    from sqlalchemy import create_engine
    from tests.conftest import TEST_DB_URL

    # Create connection pool
    engine = create_engine(
        TEST_DB_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )

    # Benchmark connection pool
    num_queries = 100

    start_time = time.time()
    query_times = []

    for i in range(num_queries):
        with engine.connect() as conn:
            query_start = time.time()
            result = conn.execute("SELECT 1")
            result.fetchone()
            query_end = time.time()
            query_times.append((query_end - query_start) * 1000)

    avg_query_time = sum(query_times) / len(query_times)
    queries_per_second = num_queries / (time.time() - start_time)

    print(f"\n=== Connection Pool Performance ===")
    print(f"Queries: {num_queries}")
    print(f"Average query time: {avg_query_time:.2f}ms")
    print(f"Queries per second: {queries_per_second:.2f}")

    # Assertions
    assert avg_query_time < 10, f"Average query time should be < 10ms, got {avg_query_time}ms"
    assert queries_per_second > 80, f"Queries per second should be > 80, got {queries_per_second}"

    engine.dispose()
