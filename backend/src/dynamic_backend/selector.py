"""
动态后端选择器
功能：
1. 时间段路由
2. 灰度发布
3. 熔断降级
4. 日志记录
5. 监控告警
"""

import logging
import time
from datetime import datetime, time as dt_time
from typing import Dict, List, Optional, Tuple
import random
import threading
from dataclasses import dataclass
from enum import Enum


logger = logging.getLogger(__name__)


class BackendStatus(Enum):
    """后端状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CIRCUIT_OPEN = "circuit_open"


@dataclass
class BackendConfig:
    """后端配置"""
    name: str
    url: str
    weight: int = 100  # 权重（用于灰度）
    timeout: int = 30   # 超时时间（秒）
    max_retries: int = 3
    priority: int = 0   # 优先级
    enabled: bool = True
    tags: List[str] = None  # 标签（用于路由匹配）
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class CircuitBreakerConfig:
    """熔断器配置"""
    failure_threshold: int = 5      # 失败阈值
    success_threshold: int = 2      # 恢复阈值
    timeout: int = 60                # 熔断超时（秒）
    half_open_max_calls: int = 3     # 半开状态最大调用数


class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = BackendStatus.HEALTHY
        self.half_open_calls = 0
        self.lock = threading.Lock()
    
    def record_failure(self):
        """记录失败"""
        with self.lock:
            self.failure_count += 1
            self.success_count = 0
            self.last_failure_time = time.time()
            
            # 检查是否需要熔断
            if self.failure_count >= self.config.failure_threshold:
                self.state = BackendStatus.CIRCUIT_OPEN
                logger.warning(
                    f"🔴 Circuit breaker opened: "
                    f"failures={self.failure_count}, "
                    f"threshold={self.config.failure_threshold}"
                )
    
    def record_success(self):
        """记录成功"""
        with self.lock:
            if self.state == BackendStatus.CIRCUIT_OPEN:
                return  # 熔断状态下不处理成功
            
            self.success_count += 1
            self.failure_count = 0
            
            # 检查是否可以从半开状态恢复
            if self.state == BackendStatus.DEGRADED:
                if self.success_count >= self.config.success_threshold:
                    self.state = BackendStatus.HEALTHY
                    logger.info(
                        f"🟢 Circuit breaker closed: "
                        f"successes={self.success_count}"
                    )
    
    def can_request(self) -> bool:
        """检查是否可以请求"""
        with self.lock:
            if self.state == BackendStatus.HEALTHY:
                return True
            
            if self.state == BackendStatus.CIRCUIT_OPEN:
                # 检查是否可以进入半开状态
                if time.time() - self.last_failure_time > self.config.timeout:
                    self.state = BackendStatus.DEGRADED
                    self.half_open_calls = 0
                    logger.info("🟡 Circuit breaker entering half-open state")
                    return True
                return False
            
            if self.state == BackendStatus.DEGRADED:
                # 半开状态限制调用次数
                if self.half_open_calls >= self.config.half_open_max_calls:
                    return False
                self.half_open_calls += 1
                return True
            
            return False
    
    def get_state(self) -> BackendStatus:
        """获取当前状态"""
        with self.lock:
            return self.state


class HealthChecker:
    """后端健康检查器"""
    
    def __init__(self, check_interval: int = 30, timeout: int = 5):
        self.check_interval = check_interval
        self.timeout = timeout
        self.health_status: Dict[str, bool] = {}
        self.last_check_time: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
    
    def check_backend(self, backend: BackendConfig) -> bool:
        """检查后端健康状态"""
        try:
            import requests
            
            response = requests.get(
                f"{backend.url}/health",
                timeout=self.timeout
            )
            
            is_healthy = response.status_code == 200
            
            with self.lock:
                self.health_status[backend.name] = is_healthy
                self.last_check_time[backend.name] = time.time()
            
            return is_healthy
            
        except Exception as e:
            with self.lock:
                self.health_status[backend.name] = False
                self.last_check_time[backend.name] = time.time()
            
            logger.error(f"❌ Health check failed for {backend.name}: {e}")
            return False
    
    def get_health_status(self, backend_name: str) -> Optional[bool]:
        """获取健康状态"""
        with self.lock:
            return self.health_status.get(backend_name)
    
    def start_periodic_check(self, backends: List[BackendConfig]):
        """启动周期性健康检查"""
        if self.running:
            return
        
        self.running = True
        
        def check_loop():
            while self.running:
                for backend in backends:
                    self.check_backend(backend)
                
                time.sleep(self.check_interval)
        
        self.thread = threading.Thread(target=check_loop, daemon=True)
        self.thread.start()
        
        logger.info(
            f"🔄 Health checker started: "
            f"interval={self.check_interval}s, "
            f"backends={len(backends)}"
        )
    
    def stop(self):
        """停止健康检查"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            logger.info("🛑 Health checker stopped")


class TimeBasedRouting:
    """基于时间的路由"""
    
    def __init__(self, time_ranges: List[Dict]):
        self.time_ranges = time_ranges
    
    def select_backend(self, backends: List[BackendConfig]) -> Optional[BackendConfig]:
        """根据时间选择后端"""
        now = datetime.now().time()
        
        for range_config in self.time_ranges:
            start = dt_time.fromisoformat(range_config['start'])
            end = dt_time.fromisoformat(range_config['end'])
            backend_name = range_config['backend']
            
            if start <= now < end:
                for backend in backends:
                    if backend.name == backend_name:
                        logger.info(
                            f"⏰ Time-based routing selected: {backend.name} "
                            f"({range_config['name']})"
                        )
                        return backend
        
        return None


class CanaryRelease:
    """灰度发布"""
    
    def __init__(self, percentage: int = 100):
        """
        Args:
            percentage: 流量百分比（0-100）
        """
        self.percentage = max(0, min(100, percentage))
    
    def should_route(self, key: Optional[str] = None) -> bool:
        """
        判断是否应该路由到新版本
        
        Args:
            key: 路由键（可以是用户ID、请求ID等）
        
        Returns:
            是否路由到新版本
        """
        if key is None:
            # 随机路由
            return random.random() * 100 < self.percentage
        
        # 基于key的一致性路由
        # 使用hash确保同一key总是路由到同一后端
        hash_value = hash(key)
        return (hash_value % 100) < self.percentage
    
    def set_percentage(self, percentage: int):
        """设置流量百分比"""
        self.percentage = max(0, min(100, percentage))
        logger.info(f"📊 Canary release percentage updated: {self.percentage}%")


class DynamicBackendSelector:
    """动态后端选择器（核心类）"""
    
    def __init__(
        self,
        backends: List[BackendConfig],
        default_backend: str,
        circuit_breaker_config: Optional[CircuitBreakerConfig] = None,
        health_check_interval: int = 30
    ):
        """
        Args:
            backends: 后端配置列表
            default_backend: 默认后端名称
            circuit_breaker_config: 熔断器配置
            health_check_interval: 健康检查间隔（秒）
        """
        self.backends = {b.name: b for b in backends}
        self.default_backend_name = default_backend
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.health_checker = HealthChecker(check_interval=health_check_interval)
        self.time_based_routing = None
        self.canary_release: Optional[CanaryRelease] = None
        self.fallback_backend: Optional[str[BackendConfig] = None
        
        # 初始化熔断器
        if circuit_breaker_config:
            for backend in backends:
                self.circuit_breakers[backend.name] = CircuitBreaker(
                    circuit_breaker_config
                )
        
        # 启动健康检查
        self.health_checker.start_periodic_check(backends)
        
        logger.info(
            f"🚀 Dynamic backend selector initialized: "
            f"backends={len(backends)}, "
            f"default={default_backend}"
        )
    
    def set_time_based_routing(self, time_ranges: List[Dict]):
        """设置基于时间的路由"""
        self.time_based_routing = TimeBasedRouting(time_ranges)
        logger.info(f"⏰ Time-based routing enabled: {len(time_ranges)} ranges")
    
    def set_canary_release(self, percentage: int, new_backend: str):
        """设置灰度发布"""
        self.canary_release = CanaryRelease(percentage)
        self.fallback_backend = new_backend
        logger.info(
            f"📊 Canary release enabled: "
            f"percentage={percentage}%, "
            f"new_backend={new_backend}"
        )
    
    def update_canary_percentage(self, percentage: int):
        """更新灰度发布百分比"""
        if self.canary_release:
            self.canary_release.set_percentage(percentage)
    
    def select_backend(
        self,
        routing_key: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Tuple[BackendConfig, str]:
        """
        选择后端
        
        Args:
            routing_key: 路由键（用于灰度发布的一致性路由）
            tags: 标签过滤
        
        Returns:
            (后端配置, 选择原因)
        """
        selected_backend = None
        reason = "default"
        
        # 1. 时间段路由
        if self.time_based_routing:
            selected_backend = self.time_based_routing.select_backend(
                list(self.backends.values())
            )
            if selected_backend:
                reason = "time_based"
        
        # 2. 灰度发布路由
        if selected_backend is None and self.canary_release and self.fallback_backend:
            if self.canary_release.should_route(routing_key):
                selected_backend = self.backends.get(self.fallback_backend)
                if selected_backend:
                    reason = "canary_release"
        
        # 3. 默认后端
        if selected_backend is None:
            selected_backend = self.backends.get(self.default_backend_name)
            if selected_backend:
                reason = "default"
        
        # 4. 熔断器检查
        if selected_backend:
            circuit_breaker = self.circuit_breakers.get(selected_backend.name)
            if circuit_breaker and not circuit_breaker.can_request():
                # 熔断器开启，需要切换到备用后端
                logger.warning(
                    f"🔴 Circuit breaker opened for {selected_backend.name}, "
                    f"selecting fallback backend"
                )
                selected_backend = self._select_fallback_backend(selected_backend)
                reason = "circuit_breaker_fallback"
        
        if selected_backend:
            logger.info(
                f"✅ Backend selected: {selected_backend.name} "
                f"({reason}) -> {selected_backend.url}"
            )
            return selected_backend, reason
        
        raise Exception("No healthy backend available")
    
    def _select_fallback_backend(self, exclude: BackendConfig) -> Optional[BackendConfig]:
        """选择备用后端"""
        for backend in self.backends.values():
            if backend.name == exclude.name:
                continue
            
            # 检查健康状态
            if not self.health_checker.get_health_status(backend.name):
                continue
            
            # 检查熔断器状态
            circuit_breaker = self.circuit_breakers.get(backend.name)
            if circuit_breaker and not circuit_breaker.can_request():
                continue
            
            return backend
        
        return None
    
    def record_success(self, backend_name: str):
        """记录成功"""
        circuit_breaker = self.circuit_breakers.get(backend_name)
        if circuit_breaker:
            circuit_breaker.record_success()
    
    def record_failure(self, backend_name: str):
        """记录失败"""
        circuit_breaker = self.circuit_breakers.get(backend_name)
        if circuit_breaker:
            circuit_breaker.record_failure()
    
    def get_backend_status(self) -> Dict[str, Dict]:
        """获取所有后端状态"""
        status = {}
        
        for name, backend in self.backends.items():
            circuit_breaker = self.circuit_breakers.get(name)
            health_status = self.health_checker.get_health_status(name)
            
            status[name] = {
                'url': backend.url,
                'enabled': backend.enabled,
                'healthy': health_status,
                'circuit_state': circuit_breaker.get_state().value if circuit_breaker else 'N/A',
                'last_check': self.health_checker.last_check_time.get(name),
            }
        
        return status
    
    def shutdown(self):
        """关闭选择器"""
        self.health_checker.stop()
        logger.info("🛑 Dynamic backend selector shutdown")
