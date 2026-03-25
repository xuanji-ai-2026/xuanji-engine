"""
Task Queue Implementation Module
Author: 吴存真 (Employee ID: 112)
Group: XJ-02 禄存星
Task: 任务队列实现
"""

from typing import Dict, List, Any, Optional
from collections import deque
from enum import Enum
import time


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """Task data class."""
    
    def __init__(self, task_id: str, name: str, priority: TaskPriority = TaskPriority.NORMAL):
        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None


class TaskQueue:
    """Task Queue Implementation"""
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize the task queue.
        
        Args:
            max_size: Maximum queue size
        """
        self.queues: Dict[TaskPriority, deque] = {
            priority: deque() for priority in TaskPriority
        }
        self.max_size = max_size
        self.completed_tasks: List[Task] = []
        
    def enqueue(self, task: Task) -> bool:
        """
        Add task to queue.
        
        Args:
            task: Task to add
            
        Returns:
            True if successful
        """
        total_size = sum(len(q) for q in self.queues.values())
        if total_size >= self.max_size:
            return False
            
        self.queues[task.priority].append(task)
        return True
        
    def dequeue(self) -> Optional[Task]:
        """
        Get highest priority task.
        
        Returns:
            Task or None
        """
        for priority in sorted(TaskPriority, reverse=True):
            if self.queues[priority]:
                task = self.queues[priority].popleft()
                task.status = TaskStatus.RUNNING
                task.started_at = time.time()
                return task
                
        return None
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "queue_sizes": {p.name: len(q) for p, q in self.queues.items()},
            "completed": len(self.completed_tasks),
            "max_size": self.max_size
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "TaskQueue",
            "version": "1.0.0",
            "status": "ready"
        }
# Performance optimization applied
