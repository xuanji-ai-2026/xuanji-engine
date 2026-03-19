"""
Task Scheduler Module
Author: 郑存义 (Employee ID: 113)
Group: XJ-02 禄存星
Task: 任务调度器
"""

from typing import Dict, List, Any, Optional, Callable
import time
from threading import Thread, Lock


class Scheduler:
    """Task Scheduler Implementation"""
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize the scheduler.
        
        Args:
            max_workers: Maximum number of workers
        """
        self.max_workers = max_workers
        self.workers: List[Thread] = []
        self.tasks: List[Callable] = []
        self.results: Dict[int, Any] = {}
        self.lock = Lock()
        self.running = False
        
    def schedule(self, task: Callable, *args, **kwargs) -> int:
        """
        Schedule a task for execution.
        
        Args:
            task: Task function
            *args: Task arguments
            **kwargs: Task keyword arguments
            
        Returns:
            Task ID
        """
        task_id = len(self.tasks)
        
        def wrapped_task():
            result = task(*args, **kwargs)
            with self.lock:
                self.results[task_id] = result
                
        self.tasks.append(wrapped_task)
        return task_id
        
    def start(self) -> None:
        """Start the scheduler."""
        self.running = True
        
        for _ in range(self.max_workers):
            worker = Thread(target=self._worker)
            worker.start()
            self.workers.append(worker)
            
    def _worker(self) -> None:
        """Worker thread function."""
        while self.running:
            with self.lock:
                if self.tasks:
                    task = self.tasks.pop(0)
                    task()
                    
            time.sleep(0.1)
            
    def get_result(self, task_id: int) -> Optional[Any]:
        """Get task result."""
        with self.lock:
            return self.results.get(task_id)
            
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "workers": len(self.workers),
            "pending_tasks": len(self.tasks),
            "completed_tasks": len(self.results),
            "running": self.running
        }
        
    def get_module_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "Scheduler",
            "version": "1.0.0",
            "status": "ready"
        }
