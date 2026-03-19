"""
禄存星（调度层）- 任务队列管理
版本: v2.0
负责人: 钱存信 (115)
功能: 任务队列、优先级调度
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class QueueTask:
    task_id: str
    priority: int
    data: Dict
    created_at: datetime

class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
    
    async def enqueue(self, task: QueueTask):
        await self.queue.put((task.priority, task))
    
    async def dequeue(self) -> Optional[QueueTask]:
        if self.queue.empty():
            return None
        _, task = await self.queue.get()
        return task

class PriorityScheduler:
    """优先级调度器"""
    
    async def schedule(self, tasks: List[QueueTask]) -> List[QueueTask]:
        return sorted(tasks, key=lambda t: t.priority)

__all__ = ["QueueTask", "TaskQueue", "PriorityScheduler"]
