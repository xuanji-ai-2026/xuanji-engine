# 动态后端选择器 - 完整文档

## 📋 概述

一个功能完整的动态后端选择系统，支持：

- ✅ **时间段路由**：根据时间段选择不同后端
- ✅ **灰度发布**：按比例分配流量到新版本
- ✅ **熔断降级**：后端不可用时自动切换
- ✅ **日志记录**：详细记录所有切换和错误
- ✅ **监控告警**：健康检查和状态监控
- ✅ **Django REST Framework 集成**：开箱即用

---

## 🚀 快速开始

### 1. 安装

```bash
pip install requests
```

### 2. 配置后端

```python
from dynamic_backend import DynamicBackendSelector, BackendConfig

# 创建后端配置
backends = [
    BackendConfig(
        name='local',
        url='http://localhost:8000',
        weight=50,
    ),
    BackendConfig(
        name='production',
        url='http://backend:8000',
        weight=100,
    ),
]

# 创建选择器
selector = DynamicBackendSelector(
    backends=backends,
    default_backend='production',
    health_check_interval=30,  # 30秒健康检查
)
```

### 3. 选择后端

```python
# 选择后端
backend, reason = selector.select_backend()

# 发送请求
import requests
response = requests.get(f"{backend.url}/api/data/")

# 记录结果
if response.ok:
    selector.record_success(backend.name)
else:
    selector.record_failure(backend.name)
```

---

## ⏰ 时间段路由

### 配置

```python
# 配置时间段路由
selector.set_time_based_routing([
    {
        'name': '工作时间',
        'backend': 'local',
        'start': '09:00:00',
        'end': '18:00:00',
    },
    {
        'name': '测试时间',
        'backend': 'test',
        'start': '18:00:00',
        'end': '22:00:00',
    },
])
```

### 工作原理

- 根据当前时间自动选择对应的后端
- 不在配置时间段内时使用默认后端
- 支持跨天时间段

---

## 📊 灰度发布

### 配置

```python
# 配置灰度发布（10%流量到test后端）
selector.set_canary_release(percentage=10, new_backend='test')
```

### 更新流量比例

```python
# 更新为50%流量
selector.update_canary_percentage(50)
```

### 一致性路由

```python
# 基于用户ID的一致性路由
backend, reason = selector.select_backend(
    routing_key=str(user.id)  # 同一用户总是路由到同一后端
)

# 随机路由
backend, reason = selector.select_backend()
```

---

## 🔴 熔断降级

### 配置

```python
from dynamic_backend import CircuitBreakerConfig

circuit_config = CircuitBreakerConfig(
    failure_threshold=5,      # 5次失败后熔断
    success_threshold=2,        # 2次成功后恢复
    timeout=60,                # 熔断60秒
    half_open_max_calls=3,      # 半开状态最多3次调用
)

selector = DynamicBackendSelector(
    backends=backends,
    default_backend='production',
    circuit_breaker_config=circuit_config,
)
```

### 状态机

```
健康 → 失败 → 失败 → ... → 熔断（阈值达到）
熔断 → 等待 → 半开（允许少量请求测试）
半开 → 成功 → 成功 → 健康（恢复成功）
半开 → 失败 → 熔断（失败，重新熔断）
```

---

## 🏥 Django REST Framework 集成

### 1. 配置

```python
# views.py
from dynamic_backend.drf_integration import DynamicBackendViewSet

class MyViewSet(DynamicBackendViewSet):
    """你的ViewSet，继承自DynamicBackendViewSet"""

    
    def list(self, request):
        # 自动选择后端并转发请求
        return self._make_request(
            'GET',
            '/api/data/',
            params=request.query_params,
        )
    
    def create(self, request):
        return self._make_request(
            'POST',
            '/api/data/',
            json=request.data,
        )
```

### 2. 注册路由

```python
# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', MyViewSet, basename='items')

urlpatterns = router.urls
```

### 3. 测试

```bash
# 查看后端状态
curl http://localhost:8000/api/items/backend_status/

# 更新灰度发布比例
curl -X POST http://localhost:8000/api/items/canary_test/ \
  -H "Content-Type: application/json" \
  -d '{"percentage": 50}'

# 测试健康检查
curl http://localhost:8000/api/items/health/
```

---

## 📝 日志记录

所有操作都会自动记录到日志：

```
🚀 Dynamic backend selector initialized: backends=3, default=production
🔄 Health checker started: interval=30s, backends=3
✅ Backend selected: local (time_based) -> http://localhost:8000
🟢 Circuit breaker closed: successes=2
🔴 Circuit breaker opened: failures=5, threshold=5
🟡 Circuit breaker entering half-open state
📊 Canary release percentage updated: 50%
```

### 配置日志

```python
import logging

# 配日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# 输出到文件
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend_selector.log'),
        logging.StreamHandler(),
    ],
)
```

---

## 📊 监控告警

### 获取后端状态

```python
# 获取所有后端状态
status = selector.get_backend_status()

for name, info in status.items():
    print(f"{name}:")
    print(f"  URL: {info['url']}")
    print(f"  健康: {info['healthy']}")
    print(f"  熔断状态: {info['circuit_state']}")
    print(f"  最后检查: {info['last_check']}")
```

### 集成到监控系统

```python
# 导出到Prometheus
from prometheus_client import Gauge

backend_healthy = Gauge(
    'backend_healthy',
    'Backend health status',
    ['backend_name']
)

for name, info in status.items():
    backend_healthy.labels(backend_name=name).set(
        1 if info['healthy'] else 0
    )
```

---

## 🎯 最佳实践

### 1. 后端命名规范

```python
# 推荐命名
backend_names = {
    'dev_local',      # 本地开发
    'dev_remote',     # 远程开发
    'test',           # 测试环境
    'staging',        # 预发布
    'production',     # 生产环境
    'fallback',       # 备用
}
```

### 2. 超时配置

```python
# 根据业务特点设置合理的超时
backends = [
    BackendConfig(
        name='fast_api',
        url='http://fast-api:8000',
        timeout=5,   # 快速接口，短超时
    ),
    BackendConfig(
        name='slow_api',
        url='http://slow-api:8000',
        timeout=30,  # 慢速接口，长超时
    ),
]
```

### 3. 熔断器阈值

```python
# 根据业务重要程度设置
circuit_config = CircuitBreakerConfig(
    failure_threshold=3,   # 核心业务，快速熔断
    success_threshold=1,     # 快速恢复
    timeout=30,             # 30秒后尝试恢复
)
```

### 4. 灰度发布策略

```python
# 分阶段灰度
stages = [10, 25, 50, 75, 100]

for percentage in stages:
    selector.update_canary_percentage(percentage)
    print(f"✅ 灰度发布比例更新为: {percentage}%")
    
    # 等待观察
    time.sleep(3600)  # 1小时
```

---

## 🐛 故障排查

### 问题1: 后端总是选择默认后端

**原因**: 时间段配置不正确，或不在配置时间段内

**解决**: 检查时间段配置，确保时间格式正确

### 问题2: 熔断器频繁熔断

**原因**: 失败阈值设置过低，或后端确实不稳定

**解决**: 提高失败阈值，或检查后端健康状态

### 问题3: 灰度发布不生效

**原因**: 百分比设置为0或100，或流量比例计算错误

**解决**: 检查灰度发布配置，确保百分比在0-100之间

---

## 📞 技术支持

- **文档位置**: `backend/src/dynamic_backend/`
- **示例代码**: `backend/src/dynamic_backend/drf_integration.py`
- **日志文件**: `backend_selector.log`

---

**Happy Routing!** 🚀
