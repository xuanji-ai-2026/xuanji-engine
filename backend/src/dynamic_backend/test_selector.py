"""
动态后端选择器测试
"""

import time
from dynamic_backend.selector import (
    DynamicBackendSelector,
    BackendConfig,
    CircuitBreakerConfig,
)


def test_basic_routing():
    """测试基本路由"""
    print("="*60)
    print("测试1: 基本路由")
    print("="*60)
    
    backends = [
        BackendConfig(name='backend1', url='http://localhost:8001'),
        BackendConfig(name='backend2', url='http://localhost:8002'),
    ]
    
    selector = DynamicBackendSelector(
        backends=backends,
        default_backend='backend1',
    )
    
    # 选择后端
    backend, reason = selector.select_backend()
    print(f"✅ 选中后端: {backend.name}")
    print(f"   原因: {reason}")
    print()


def test_circuit_breaker():
    """测试熔断器"""
    print("="*60)
    print("测试2: 熔断器")
    print("="*60)
    
    backends = [
        BackendConfig(name='test_backend', url='http://localhost:8000'),
    ]
    
    circuit_config = CircuitBreakerConfig(
        failure_threshold=3,
        success_threshold=2,
        timeout=60,
    )
    
    selector = DynamicBackendSelector(
        backends=backends,
        default_backend='test_backend',
        circuit_breaker_config=circuit_config,
    )
    
    backend, reason = selector.select_backend()
    print(f"✅ 初始状态: {selector.circuit_breakers['test_backend'].get_state().value}")
    
    # 模拟失败
    print("模拟3次失败...")
    for i in range(3):
        selector.record_failure('test_backend')
        print(f"   失败 {i+1}: {selector.circuit_breakers['test_backend'].get_state().value}")
    
    # 检查是否可以请求
    can_request = selector.circuit_breakers['test_backend'].can_request()
    print(f"✅ 熔断后是否可请求: {can_request}")
    print()


def test_canary_release():
    """测试灰度发布"""
    print("="*60)
    print("测试3: 灰度发布")
    print("="*60)
    
    backends = [
        BackendConfig(name='old_backend', url='http://localhost:8001'),
        BackendConfig(name='new_backend', url='http://localhost:8002'),
    ]
    
    selector = DynamicBackendSelector(
        backends=backends,
        default_backend='old_backend',
    )
    
    # 配置灰度发布（30%流量）
    selector.set_canary_release(percentage=30, new_backend='new_backend')
    
    print("测试100次选择...")
    new_count = 0
    old_count = 0
    
    for i in range(100):
        backend, reason = selector.select_backend()
        if backend.name == 'new_backend':
            new_count += 1
        else:
            old_count += 1
    
    print(f"✅ new_backend: {new_count}次 ({new_count}%)")
    print(f"✅ old_backend: {old_count}次 ({old_count}%)")
    print()


def test_time_based_routing():
    """测试时间段路由"""
    print("="*60)
    print("测试4: 时间段路由")
    print("="*60)
    
    backends = [
        BackendConfig(name='work_backend', url='http://localhost:8001'),
        BackendConfig(name='test_backend', url='http://localhost:8002'),
    ]
    
    selector = DynamicBackendSelector(
        backends=backends,
        default_backend='work_backend',
    )
    
    # 配置当前时间附近的时间段
    from datetime import datetime, timedelta
    now = datetime.now()
    start = (now - timedelta(minutes=30)).strftime('%H:%M:%S')
    end = (now + timedelta(minutes=30)).strftime('%H:%M:%S')
    
    selector.set_time_based_routing([
        {
            'name': '当前时间段',
            'backend': 'work_backend',
            'start': start,
            'end': end,
        },
    ])
    
    backend, reason = selector.select_backend()
    print(f"✅ 当前时间选中: {backend.name}")
    print(f"   原因: {reason}")
    print()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("动态后端选择器测试")
    print("="*60 + "\n")
    
    test_basic_routing()
    test_circuit_breaker()
    test_canary_release()
    test_time_based_routing()
    
    print("="*60)
    print("所有测试完成！")
    print("="*60)
