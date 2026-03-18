"""
Memory Storage Implementation Module
Author: 沈巨明 (Employee ID: 120)
Group: XJ-03 巨门星
Task: 记忆存储实现
"""

from typing import Dict, List, Any, Optional
import time
import json


class MemoryStore:
    """Memory Storage Implementation"""
    
    def __init__(self):
        """Initialize the memory store."""
        self.short_term: Dict[str, Any] = {}
        self.long_term: Dict[str, List[Any]] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        
    def store(self, key: str, value: Any, memory_type: str = "short") -> bool:
        """
        Store memory.
        
        Args:
            key: Memory key
            value: Memory value
            memory_type: Type of memory (short/long)
            
        Returns:
            True if successful
        """
        try:
            if memory_type == "short":
                self.short_term[key] = value
            else:
                if key not in self.long_term:
                    self.long_term[key] = []
                self.long_term[key].append(value)
                
            self.metadata[key] = {
                "type": memory_type,
                "created_at": time.time(),
                "updated_at": time.time()
            }
            
            return True
        except Exception:
            return False
            
    def retrieve(self, key: str, memory_type: Optional[str] = None) -> Optional[Any]:
        """
        Retrieve memory.
        
        Args:
            key: Memory key
            memory_type: Type of memory (optional)
            
        Returns:
            Memory value or None
        """
        if memory_type == "short" or memory_type is None:
            if key in self.short_term:
                return self.short_term[key]
                
        if memory_type == "long" or memory_type is None:
            if key in self.long_term:
                return self.long_term[key]
                
        return None
        
    def delete(self, key: str) -> bool:
        """Delete memory."""
        if key in self.short_term:
            del self.short_term[key]
            
        if key in self.long_term:
            del self.long_term[key]
            
        if key in self.metadata:
            del self.metadata[key]
            
        return True
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "metadata_count": len(self.metadata)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "MemoryStore",
            "version": "1.0.0",
            "status": "ready"
        }
