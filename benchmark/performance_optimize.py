"""
Performance Optimization and Monitoring
"""
import pytest


@pytest.mark.benchmark
def test_performance_bottleneck_analysis():
    """Analyze performance bottlenecks."""
    import time
    from src.ziwei.intent_recognition import IntentRecognition
    from src.jumen.memory_storage_shen import MemoryStorage
    from src.tanlang.dialog_manage_lei import DialogueManager

    components = {
        "IntentRecognition": IntentRecognition(),
        "MemoryStorage": MemoryStorage(),
        "DialogueManager": DialogueManager()
    }

    print("\n=== Performance Bottleneck Analysis ===")

    # Measure each component
    for name, component in components.items():
        start = time.time()
        num_iterations = 100

        for i in range(num_iterations):
            if name == "IntentRecognition":
                component.recognize("测试文本")
            elif name == "MemoryStorage":
                component.store(None, {
                    "user_id": "test_user",
                    "content": "测试内容",
                    "type": "preference"
                })
            elif name == "DialogueManager":
                component.generate_response("intent", "user")

        end = time.time()
        total_time = end - start
        avg_time = (total_time / num_iterations) * 1000

        print(f"{name}:")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Average time: {avg_time:.2f}ms")
        print(f"  Operations/second: {num_iterations/total_time:.2f}")

        # Identify bottlenecks
        if avg_time > 50:
            print(f"  ⚠️  BOTTLENECK: Average time > 50ms")
            if name == "IntentRecognition":
                print(f"     Optimization: Cache model predictions, use batch processing")
            elif name == "MemoryStorage":
                print(f"     Optimization: Use connection pooling, add cache layer")
            elif name == "DialogueManager":
                print(f"     Optimization: Cache dialogue responses, use async operations")


@pytest.mark.benchmark
def test_cache_hit_rate():
    """Test cache hit rate and effectiveness."""
    import time
    from src.ziwei.intent_recognition import IntentRecognition

    recognizer = IntentRecognition()

    print("\n=== Cache Hit Rate Analysis ===")

    # First access (cache miss)
    start = time.time()
    result1 = recognizer.recognize("测试文本1")
    time1 = (time.time() - start) * 1000

    # Second access (cache hit)
    start = time.time()
    result2 = recognizer.recognize("测试文本1")
    time2 = (time.time() - start) * 1000

    cache_improvement = ((time1 - time2) / time1) * 100

    print(f"First access (miss): {time1:.2f}ms")
    print(f"Second access (hit): {time2:.2f}ms")
    print(f"Cache improvement: {cache_improvement:.2f}%")

    if cache_improvement > 0:
        print("✓ Cache is effective")
    else:
        print("⚠️  Cache not working properly")


@pytest.mark.benchmark
def test_memory_usage():
    """Test memory usage during operations."""
    import tracemalloc
    import time

    from src.ziwei.intent_recognition import IntentRecognition

    recognizer = IntentRecognition()

    print("\n=== Memory Usage Analysis ===")

    # Baseline memory
    tracemalloc.start()
    baseline = tracemalloc.get_traced_memory()[0]

    # Perform operations
    for i in range(100):
        recognizer.recognize(f"测试文本{i}")

    # Measure memory
    current = tracemalloc.get_traced_memory()[0]
    memory_used = current - baseline

    tracemalloc.stop()

    print(f"Baseline memory: {baseline / 1024:.2f} KB")
    print(f"Current memory: {current / 1024:.2f} KB")
    print(f"Memory used: {memory_used / 1024:.2f} KB")

    if memory_used > 10 * 1024:  # More than 10MB
        print(f"⚠️  HIGH MEMORY USAGE: {memory_used / 1024:.2f} KB")
        print("   Optimization: Add memory limit, optimize data structures")
    else:
        print("✓ Memory usage within acceptable range")


@pytest.mark.benchmark
def test_cpu_usage():
    """Test CPU usage during operations."""
    import psutil
    import time

    print("\n=== CPU Usage Analysis ===")

    # Get baseline CPU
    cpu_percent_before = psutil.cpu_percent(interval=1)

    # Perform CPU-intensive operations
    from src.ziwei.intent_recognition import IntentRecognition
    recognizer = IntentRecognition()

    start_time = time.time()
    for i in range(100):
        recognizer.recognize(f"测试文本{i}")
    end_time = time.time()

    # Get CPU during operations
    cpu_percent_during = psutil.cpu_percent(interval=1)

    operations_per_second = 100 / (end_time - start_time)

    print(f"CPU before: {cpu_percent_before:.2f}%")
    print(f"CPU during: {cpu_percent_during:.2f}%")
    print(f"Operations: 100")
    print(f"Time: {end_time - start_time:.3f}s")
    print(f"Operations/second: {operations_per_second:.2f}")

    if cpu_percent_during > 80:
        print("⚠️  HIGH CPU USAGE")
        print("   Optimization: Use async operations, implement rate limiting")


@pytest.mark.benchmark
def test_concurrent_request_performance():
    """Test performance under concurrent requests."""
    import asyncio
    import time

    print("\n=== Concurrent Request Performance ===")

    async def simulate_request(request_id):
        """Simulate a request."""
        # Simulate processing time
        await asyncio.sleep(0.01)
        return {"request_id": request_id, "status": "success"}

    async def test_concurrency(concurrent_requests):
        """Test with different concurrency levels."""
        start_time = time.time()
        results = await asyncio.gather(*[
            simulate_request(i) for i in range(concurrent_requests)
        ])
        total_time = time.time() - start_time

        success_rate = len(results) / concurrent_requests * 100
        avg_time = (total_time / concurrent_requests) * 1000

        print(f"Concurrency: {concurrent_requests}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Average time: {avg_time:.2f}ms")

        return total_time

    # Test with different concurrency levels
    for concurrency in [10, 50, 100]:
        total_time = asyncio.run(test_concurrency(concurrency))
        print()


@pytest.mark.benchmark
def test_optimization_recommendations():
    """Generate optimization recommendations."""
    print("\n=== Optimization Recommendations ===")

    recommendations = {
        "Caching": [
            "Implement response caching for common queries",
            "Use Redis for session storage",
            "Cache model predictions"
        ],
        "Database": [
            "Use connection pooling",
            "Add database indexes for frequent queries",
            "Implement query result caching"
        ],
        "API": [
            "Implement rate limiting",
            "Use compression for large responses",
            "Optimize JSON serialization"
        ],
        "Memory": [
            "Implement object pooling",
            "Use generators instead of lists",
            "Limit memory usage per request"
        ],
        "Async": [
            "Use async/await for I/O operations",
            "Implement concurrent request handling",
            "Use async database drivers"
        ]
    }

    for category, items in recommendations.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")

    print("\n=== Priority Recommendations ===")
    print("1. Implement Redis caching for common queries")
    print("2. Add database connection pooling")
    print("3. Implement async database operations")
    print("4. Add API rate limiting")
    print("5. Optimize memory usage")
