"""
Memory Retrieve Implementation Module
Author: 韩巨亮 (Employee ID: 121)
Group: XJ-03 巨门星
Task: 记忆检索实现
"""

from typing import Dict, List, Any, Optional
import time


class MemoryRetrieve:
    """Memory Retrieve Implementation"""
    
    def __init__(self, memory_store):
        """
        Initialize the memory retrieve module.
        
        Args:
            memory_store: MemoryStore instance
        """
        self.memory_store = memory_store
        self.index: Dict[str, List[str]] = {}
        
    def index_memory(self, key: str, keywords: List[str]) -> None:
        """
        Index memory for faster retrieval.
        
        Args:
            key: Memory key
            keywords: Keywords to index
        """
        for keyword in keywords:
            if keyword not in self.index:
                self.index[keyword] = []
            if key not in self.index[keyword]:
                self.index[keyword].append(key)
                
    def retrieve_by_key(self, key: str) -> Optional[Any]:
        """Retrieve by key."""
        return self.memory_store.retrieve(key)
        
    def retrieve_by_keyword(self, keyword: str) -> List[Any]:
        """
        Retrieve memories by keyword.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching memories
        """
        results = []
        
        if keyword in self.index:
            for key in self.index[keyword]:
                value = self.memory_store.retrieve(key)
                if value:
                    results.append(value)
                    
        return results
        
    def retrieve_by_time(self, start_time: float, end_time: float) -> List[Any]:
        """
        Retrieve memories by time range.
        
        Args:
            start_time: Start timestamp
            end_time: End timestamp
            
        Returns:
            List of memories in time range
        """
        results = []
        
        for key, metadata in self.memory_store.metadata.items():
            created_at = metadata.get("created_at", 0)
            if start_time <= created_at <= end_time:
                value = self.memory_store.retrieve(key)
                if value:
                    results.append(value)
                    
        return results
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "index_size": len(self.index),
            "indexed_keywords": list(self.index.keys())[:10]
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "MemoryRetrieve",
            "version": "1.0.0",
            "status": "ready"
        }
