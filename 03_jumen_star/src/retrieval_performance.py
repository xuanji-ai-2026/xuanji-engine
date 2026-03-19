"""
巨门星（记忆层）- 检索性能优化
版本: v2.0
负责人: 沈巨明 (120)
功能: P95<100ms高性能检索
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import time

@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    created_at: float
    expires_at: float
    access_count: int = 0

class QueryCache:
    """查询缓存"""
    
    def __init__(self, max_size: int = 10000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, query: str, filters: Optional[Dict]) -> str:
        """生成缓存Key"""
        filter_str = str(sorted(filters.items())) if filters else ""
        return f"{query}:{filter_str}"
    
    async def get(
        self,
        query: str,
        filters: Optional[Dict] = None
    ) -> Optional[Any]:
        """获取缓存"""
        key = self._make_key(query, filters)
        
        if key in self.cache:
            entry = self.cache[key]
            current_time = time.time()
            
            if current_time < entry.expires_at:
                entry.access_count += 1
                self.hits += 1
                return entry.value
            else:
                del self.cache[key]
        
        self.misses += 1
        return None
    
    async def set(
        self,
        query: str,
        value: Any,
        filters: Optional[Dict] = None,
        ttl: Optional[int] = None
    ):
        """设置缓存"""
        key = self._make_key(query, filters)
        current_time = time.time()
        
        # 清理过期条目
        if len(self.cache) >= self.max_size:
            await self._evict_oldest()
        
        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=current_time,
            expires_at=current_time + (ttl or self.ttl)
        )
    
    async def _evict_oldest(self):
        """清理最旧条目"""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), 
                        key=lambda k: self.cache[k].created_at)
        del self.cache[oldest_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate
        }

class QueryOptimizer:
    """查询优化器"""
    
    def __init__(self):
        self.cache = QueryCache()
        self.index_hints = {}
    
    async def optimize_query(
        self,
        query: str,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """优化查询"""
        # 1. 检查缓存
        cached_result = await self.cache.get(query, filters)
        if cached_result:
            return {"result": cached_result, "source": "cache"}
        
        # 2. 生成执行计划
        plan = await self._generate_plan(query, filters)
        
        # 3. 执行查询
        result = await self._execute(plan)
        
        # 4. 缓存结果
        await self.cache.set(query, result, filters)
        
        return {"result": result, "source": "database"}
    
    async def _generate_plan(
        self,
        query: str,
        filters: Optional[Dict]
    ) -> Dict[str, Any]:
        """生成执行计划"""
        # TODO: 生成最优执行计划
        # 1. 分析查询
        # 2. 选择索引
        # 3. 优化顺序
        return {"type": "sequential"}
    
    async def _execute(self, plan: Dict) -> Any:
        """执行查询"""
        # TODO: 执行查询
        return []

class PerformanceMonitor:
    """性能监控"""
    
    def __init__(self):
        self.latencies = []
        self.max_samples = 1000
    
    async def record_latency(self, operation: str, latency_ms: float):
        """记录延迟"""
        self.latencies.append({
            "operation": operation,
            "latency": latency_ms,
            "timestamp": time.time()
        })
        
        if len(self.latencies) > self.max_samples:
            self.latencies = self.latencies[-self.max_samples:]
    
    async def get_percentile(self, percentile: float) -> float:
        """获取百分位延迟"""
        if not self.latencies:
            return 0.0
        
        sorted_latencies = sorted(
            [l["latency"] for l in self.latencies]
        )
        
        index = int(len(sorted_latencies) * percentile / 100)
        return sorted_latencies[min(index, len(sorted_latencies) - 1)]
    
    async def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        return {
            "p50": await self.get_percentile(50),
            "p95": await self.get_percentile(95),
            "p99": await self.get_percentile(99),
            "avg": sum(l["latency"] for l in self.latencies) / len(self.latencies)
            if self.latencies else 0
        }

class RetrievalPerformanceOptimizer:
    """检索性能优化系统"""
    
    def __init__(self):
        self.query_optimizer = QueryOptimizer()
        self.performance_monitor = PerformanceMonitor()
        self.target_p95_ms = 100
    
    async def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        top_k: int = 10
    ) -> Tuple[List[Any], Dict[str, Any]]:
        """检索"""
        start_time = time.time()
        
        # 执行优化查询
        result = await self.query_optimizer.optimize_query(query, filters)
        
        # 记录延迟
        latency_ms = (time.time() - start_time) * 1000
        await self.performance_monitor.record_latency("search", latency_ms)
        
        # 检查是否达标
        p95 = await self.performance_monitor.get_percentile(95)
        status = "ok" if p95 < self.target_p95_ms else "warning"
        
        return result.get("result", []), {
            "latency_ms": latency_ms,
            "p95_ms": p95,
            "status": status
        }
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """获取性能报告"""
        stats = await self.performance_monitor.get_stats()
        
        return {
            "current": stats,
            "target_p95_ms": self.target_p95_ms,
            "status": "ok" if stats["p95"] < self.target_p95_ms else "warning"
        }

# 导出
__all__ = ["QueryCache", "QueryOptimizer", "PerformanceMonitor", "RetrievalPerformanceOptimizer"]
