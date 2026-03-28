"""
动态后端选择器 - Django REST Framework 集成示例

使用示例：
1. 配置后端选择器
2. 在ViewSet中使用
3. 配置监控和日志
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
import logging
from typing import Optional

from dynamic_backend.selector import (
    DynamicBackendSelector,
    BackendConfig,
    CircuitBreakerConfig,
)


logger = logging.getLogger(__name__)


# ==================== 配置示例 ====================

def create_backend_selector() -> DynamicBackendSelector:
    """创建后端选择器实例"""
    
    # 后端配置
    backends = [
        BackendConfig(
            name='local',
            url='http://localhost:8000',
            weight=50,
            tags=['dev', 'local'],
        ),
        BackendConfig(
            name='test',
            url='http://test-backend:8000',
            weight=30,
            tags=['test'],
        ),
        BackendConfig(
            name='production',
            url='http://production-backend:8000',
            weight=100,
            priority=10,
            tags=['prod'],
        ),
        BackendConfig(
            name='fallback',
            url='http://fallback-backend:8000',
            weight=10,
            priority=1,  # 最低优先级
            tags=['fallback'],
        ),
    ]
    
    # 熔断器配置
    circuit_config = CircuitBreakerConfig(
        failure_threshold=5,      # 5次失败后熔断
        success_threshold=2,        # 2次成功后恢复
        timeout=60,                # 熔断60秒
        half_open_max_calls=3,      # 半开状态最多3次调用
    )
    
    # 创建选择器
    selector = DynamicBackendSelector(
        backends=backends,
        default_backend='production',
        circuit_breaker_config=circuit_config,
        health_check_interval=30,   # 30秒健康检查间隔
    )
    
    # 配置基于时间的路由
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
    
    # 配置灰度发布（10%流量到test后端）
    selector.set_canary_release(percentage=10, new_backend='test')
    
    return selector


# 全局选择器实例
backend_selector = create_backend_selector()


# ==================== ViewSet 使用示例 ====================

class DynamicBackendViewSet(viewsets.ViewSet):
    """
    使用动态后端选择器的ViewSet示例
    
    所有请求都会自动选择合适的后端
    """
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Response:
        """
        发送请求到动态选择的后端
        
        Args:
            method: HTTP方法（GET, POST, PUT, DELETE等）
            endpoint: API端点路径（如 /api/users/）
            **kwargs: 传递给requests的其他参数
        """
        try:
            # 选择后端
            routing_key = kwargs.pop('routing_key', None)
            backend, reason = backend_selector.select_backend(
                routing_key=routing_key
            )
            
            # 构建完整URL
            full_url = f"{backend.url}{endpoint}"
            
            # 添加自定义头
            headers = kwargs.pop.get('headers', {})
            headers.update({
                'X-Backend-Name': backend.name,
                'X-Backend-Reason': reason,
                'X-Backend-URL': backend.url,
            })
            
            # 发送请求
            response = requests.request(
                method,
                full_url,
                timeout=backend.timeout,
                headers=headers,
                **kwargs
            )
            
            # 记录成功
            backend_selector.record_success(backend.name)
            
            # 返回响应
            return Response(
                response.json(),
                status=response.status_code,
                headers={
                    'X-Backend-Used': backend.name,
                    'X-Backend-Reason': reason,
                }
            )
            
        except requests.Timeout:
            # 超时错误
            logger.error(f"⏱️ Backend timeout: {backend.name}")
            backend_selector.record_failure(backend.name)
            
            return Response(
                {'error': 'Backend timeout'},
                status=status.HTTP_504_GATEWAY_TIME_OUT
            )
        
        except requests.ConnectionError:
            # 连接错误
            logger.error(f"🔌 Backend connection error: {backend.name}")
            backend_selector.record_failure(backend.name)
            
            return Response(
                {'error': 'Backend unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        except Exception as e:
            # 其他错误
            logger.error(f"❌ Backend error: {backend.name}, {e}")
            backend_selector.record_failure(backend.name)
            
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request):
        """GET /api/data/ - 查询列表"""
        return self._make_request(
            'GET',
            '/api/data/',
            params=request.query_params,
            routing_key=request.user.id if request.user.is_authenticated else None
        )
    
    def retrieve(self, request, pk=None):
        """GET /api/data/{pk}/ - 获取详情"""
        return self._make_request(
            'GET',
            f'/api/data/{pk}/' if pk else '/api/data/',
            routing_key=request.user.id if request.user.is_authenticated else None
        )
    
    def create(self, request):
        """POST /api/data/ - 创建"""
        return self._make_request(
            'POST',
            '/api/data/',
            json=request.data,
            routing_key=request.user.id if request.user.is_authenticated else None
        )
    
    def update(self, request, pk=None):
        """PUT /api/data/{pk}/ - 更新"""
        return self._make_request(
            'PUT',
            f'/api/data/{pk}/' if pk else '/api/data/',
            json=request.data,
            routing_key=request.user.id if request.user.is_authenticated else None
        )
    
    def destroy(self, request, pk=None):
        """DELETE /api/data/{pk}/ - 删除"""
        return self._make_request(
            'DELETE',
            f'/api/data/{pk}/' if pk else '/api/data/',
            routing_key=request.user.id if request.user.is_authenticated else None
        )
    
    @action(detail=False, methods=['get'])
    def health(self, request):
        """GET /api/data/health/ - 健康检查"""
        return self._make_request(
            'GET',
            '/api/health/',
        )
    
    @action(detail=False, methods=['post'])
    def canary_test(self, request):
        """POST /api/data/canary_test/ - 灰度发布测试
        
        可以使用这个端点测试灰度发布是否工作正常
        """
        # 获取测试流量比例
        percentage = request.data.get('percentage', 10)
        
        # 更新灰度发布比例
        backend_selector.update_canary_percentage(percentage)
        
        # 返回当前状态
        return Response({
            'message': 'Canary release percentage updated',
            'percentage': percentage,
            'backend_status': backend_selector.get_backend_status()
        })
    
    @action(detail=False, methods=['get'])
    def backend_status(self, request):
        """GET /api/data/backend_status/ - 查看后端状态
        
        返回所有后端的详细状态信息
        """
        return Response(backend_selector.get_backend_status())


# ==================== Django Admin 集成示例 ====================

class BackendManagementView:
    """后端管理视图（用于Django Admin后台）"""
    
    @staticmethod
    def get_dashboard_data():
        """获取仪表盘数据"""
        status = backend_selector.get_backend_status()
        
        # 统计数据
        total = len(status)
        healthy = sum(1 for s in status.values() if s.get('healthy'))
        unhealthy = total - healthy
        circuits_open = sum(
            1 for s in status.values()
            if s.get('circuit_state') == 'circuit_open'
        )
        
        return {
            'total_backends': total,
            'healthy_backends': healthy,
            'unhealthy_backends': unhealthy,
            'circuits_open': circuits_open,
            'details': status,
        }
    
    @staticmethod
    def update_canary_percentage(percentage: int):
        """更新灰度发布百分比"""
        backend_selector.update_canary_percentage(percentage)
        return {'percentage': percentage}


# ==================== 使用示例 ====================

"""
在Django项目中使用：

1. 在 views.py 中导入：

    from your_app.views import DynamicBackendViewSet

2. 在 urls.py 中注册路由：

    from rest_framework.routers import DefaultRouter
    
    router = DefaultRouter()
    router.register(r'data', DynamicBackendViewSet, basename='data')
    
    urlpatterns = router.urls

3. 测试灰度发布：

    # 更新灰度发布比例到50%
    POST /api/data/canary_test/
    {
        "percentage": 50
    }
    
    # 查看后端状态
    GET /api/data/backend_status/
    
4. 查看日志：

    所有后端切换、熔断、健康检查都会记录到日志中
    可以使用以下命令查看日志：
    
    tail -f logs/django.log | grep "Backend"

5. 监控集成：

    可以将 get_dashboard_data() 的返回值推送到监控系统
    如 Prometheus、Grafana 等

"""
