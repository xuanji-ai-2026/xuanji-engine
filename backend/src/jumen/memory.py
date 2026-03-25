"""
玄玑引擎 - 记忆系统（巨门星）
三层记忆：瞬时/短期/长期

作者: 玄玑引擎开发团队
日期: 2026-03-17
"""

import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from collections import deque


class Message(BaseModel):
    """消息"""
    role: str = Field(..., description="角色: user/assistant/system")
    content: str = Field(..., description="内容")
    timestamp: float = Field(default_factory=lambda: time.time())


class TransientMemory:
    """
    瞬时记忆（会话级）
    使用滑动窗口保留最近N轮对话
    """
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.messages: deque = deque(maxlen=window_size)
        
    def add_message(self, role: str, content: str):
        """添加消息"""
        message = Message(role=role, content=content)
        self.messages.append(message)
        
    def get_context(self, max_tokens: int = None) -> str:
        """获取上下文"""
        messages = list(self.messages)
        context = "\n".join([
            f"{msg.role}: {msg.content}" 
            for msg in messages
        ])
        return context
    
    def clear(self):
        """清空记忆"""
        self.messages.clear()
        
    def get_messages(self) -> List[Message]:
        """获取所有消息"""
        return list(self.messages)


class ShortTermMemory:
    """
    短期记忆（任务级）
    使用Redis模拟（这里用内存）
    """
    
    def __init__(self, ttl: int = 3600):  # 默认1小时
        self.ttl = ttl
        self.storage: Dict[str, tuple[Any, float]] = {}
        
    def set(self, key: str, value: Any, ttl: int = None):
        """设置值"""
        expire_at = time.time() + (ttl or self.ttl)
        self.storage[key] = (value, expire_at)
        
    def get(self, key: str) -> Optional[Any]:
        """获取值"""
        if key not in self.storage:
            return None
            
        value, expire_at = self.storage[key]
        
        # 检查是否过期
        if time.time() > expire_at:
            del self.storage[key]
            return None
            
        return value
        
    def delete(self, key: str):
        """删除"""
        if key in self.storage:
            del self.storage[key]
            
    def cleanup(self):
        """清理过期数据"""
        now = time.time()
        expired_keys = [
            key for key, (_, exp) in self.storage.items()
            if now > exp
        ]
        for key in expired_keys:
            del self.storage[key]


class LongTermMemory:
    """
    长期记忆（永久）
    向量检索（Milvus接口）
    """
    
    def __init__(self):
        self.embeddings = []  # 模拟向量
        self.metadata = []    # 元数据
        self.next_id = 1
        
    def add(
        self,
        content: str,
        user_id: str = None,
        metadata: Dict = None
    ) -> str:
        """添加记忆"""
        memory_id = f"mem_{self.next_id}"
        self.next_id += 1
        
        # 模拟向量化
        embedding = [0.0] * 384  # 简化
        self.embeddings.append(embedding)
        
        self.metadata.append({
            "id": memory_id,
            "content": content,
            "user_id": user_id,
            "metadata": metadata or {},
            "timestamp": time.time()
        })
        
        return memory_id
    
    def search(
        self,
        query: str,
        user_id: str = None,
        top_k: int = 5
    ) -> List[Dict]:
        """语义检索"""
        # 简化实现：返回最近的内容
        results = []
        for meta in sorted(
            self.metadata,
            key=lambda x: x["timestamp"],
            reverse=True
        )[:top_k]:
            if user_id is None or meta.get("user_id") == user_id:
                results.append(meta)
                
        return results
    
    def get(self, memory_id: str) -> Optional[Dict]:
        """获取单条记忆"""
        for meta in self.metadata:
            if meta["id"] == memory_id:
                return meta
        return None
    
    def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        for i, meta in enumerate(self.metadata):
            if meta["id"] == memory_id:
                del self.embeddings[i]
                del self.metadata[i]
                return True
        return False


class MemorySystem:
    """
    统一记忆系统
    整合三层记忆
    """
    
    def __init__(
        self,
        window_size: int = 10,
        short_ttl: int = 3600
    ):
        self.transient = TransientMemory(window_size)
        self.short_term = ShortTermMemory(short_ttl)
        self.long_term = LongTermMemory()
        
    # 瞬时记忆
    def add_message(self, role: str, content: str):
        """添加会话消息"""
        self.transient.add_message(role, content)
        
    def get_context(self) -> str:
        """获取会话上下文"""
        return self.transient.get_context()
    
    # 短期记忆
    def short_set(self, key: str, value: Any, ttl: int = None):
        """短期存储"""
        self.short_term.set(key, value, ttl)
        
    def short_get(self, key: str) -> Optional[Any]:
        """短期获取"""
        return self.short_term.get(key)
        
    # 长期记忆
    def long_add(
        self,
        content: str,
        user_id: str = None,
        metadata: Dict = None
    ) -> str:
        """长期存储"""
        return self.long_term.add(content, user_id, metadata)
        
    def long_search(
        self,
        query: str,
        user_id: str = None,
        top_k: int = 5
    ) -> List[Dict]:
        """长期检索"""
        return self.long_term.search(query, user_id, top_k)


# 测试代码
if __name__ == "__main__":
    memory = MemorySystem()
    
    # 测试瞬时记忆
    memory.add_message("user", "你好，我叫张三")
    memory.add_message("assistant", "你好张三，很高兴认识你")
    print("瞬时记忆:", memory.get_context())
    
    # 测试短期记忆
    memory.short_set("current_task", "测试任务")
    print("短期记忆:", memory.short_get("current_task"))
    
    # 测试长期记忆
    memory.long_add("用户张三喜欢科幻电影", "zhangsan")
    results = memory.long_search("用户偏好", user_id="zhangsan")
    print("长期记忆搜索:", results)
