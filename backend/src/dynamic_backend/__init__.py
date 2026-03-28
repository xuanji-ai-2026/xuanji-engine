"""
动态后端选择器

提供灵活的后端路由、灰度发布、熔断降级功能
"""

from .selector import (
    DynamicBackendSelector,
    BackendConfig,
    CircuitBreakerConfig,
    CircuitBreaker,
    HealthChecker,
    TimeBasedRouting,
    CanaryRelease,
    BackendStatus,
)

__all__ = [
    'DynamicBackendSelector',
    'BackendConfig',
    'CircuitBreakerConfig',
    'CircuitBreaker',
    'HealthChecker',
    'TimeBasedRouting',
    'CanaryRelease',
    'BackendStatus',
]
