"""
Intent Interface Design Module
Author: 赵四维 (Employee ID: 109)
Group: XJ-01 紫微元灵
Task: 意图接口设计
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class IntentType(Enum):
    """Intent types enumeration."""
    SEARCH = "search"
    CREATE = "create"
    DELETE = "delete"
    UPDATE = "update"
    QUERY = "query"
    UNKNOWN = "unknown"


@dataclass
class IntentRequest:
    """Intent request data class."""
    text: str
    context: Optional[Dict[str, Any]] = None
    language: str = "en"


@dataclass
class IntentResponse:
    """Intent response data class."""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    timestamp: float


class IntentInterface:
    """Intent Interface Design Implementation"""
    
    def __init__(self):
        """Initialize the interface module."""
        self.requests: List[IntentRequest] = []
        self.responses: List[IntentResponse] = []
        
    def create_request(self, text: str, context: Optional[Dict] = None) -> IntentRequest:
        """
        Create an intent request.
        
        Args:
            text: Input text
            context: Optional context
            
        Returns:
            IntentRequest instance
        """
        request = IntentRequest(text=text, context=context)
        self.requests.append(request)
        return request
        
    def create_response(self, intent: str, confidence: float, entities: Dict) -> IntentResponse:
        """
        Create an intent response.
        
        Args:
            intent: Recognized intent
            confidence: Confidence score
            entities: Extracted entities
            
        Returns:
            IntentResponse instance
        """
        import time
        response = IntentResponse(
            intent=intent,
            confidence=confidence,
            entities=entities,
            timestamp=time.time()
        )
        self.responses.append(response)
        return response
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "requests": len(self.requests),
            "responses": len(self.responses)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "IntentInterface",
            "version": "1.0.0",
            "status": "ready"
        }
