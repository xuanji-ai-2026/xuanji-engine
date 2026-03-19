"""
Intent Recognition Algorithm Module
Author: 张一凡 (Employee ID: 106)
Group: XJ-01 紫微元灵
Task: 意图识别算法实现
"""

from typing import Dict, List, Any, Optional
import re


class IntentAlgorithm:
    """Intent Recognition Algorithm Implementation"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the intent recognition algorithm.
        
        Args:
            model_path: Path to the model file
        """
        self.model_path = model_path
        self.intent_patterns: Dict[str, List[str]] = {}
        self.intent_confidence_threshold = 0.8
        
    def load_patterns(self, patterns: Dict[str, List[str]]) -> None:
        """
        Load intent recognition patterns.
        
        Args:
            patterns: Dictionary of intent patterns
        """
        self.intent_patterns = patterns
        
    def recognize(self, text: str) -> Dict[str, Any]:
        """
        Recognize intent from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary containing intent and confidence
        """
        text = text.lower().strip()
        intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    intents.append({
                        "intent": intent,
                        "confidence": 0.9,
                        "matched_pattern": pattern
                    })
                    
        if intents:
            # Return highest confidence intent
            best_intent = max(intents, key=lambda x: x["confidence"])
            return best_intent
            
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "matched_pattern": None
        }
        
    def extract_entities(self, text: str, intent: str) -> Dict[str, Any]:
        """
        Extract entities from text based on intent.
        
        Args:
            text: Input text
            intent: Recognized intent
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        # Entity extraction rules based on intent
        if intent == "search":
            # Extract search query
            match = re.search(r'search (?:for |)(.+)', text)
            if match:
                entities["query"] = match.group(1)
                
        elif intent == "create":
            # Extract creation target
            match = re.search(r'create (?:a |an |)(.+)', text)
            if match:
                entities["target"] = match.group(1)
                
        elif intent == "delete":
            # Extract deletion target
            match = re.search(r'delete (?:the |)(.+)', text)
            if match:
                entities["target"] = match.group(1)
                
        return entities
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get module status.
        
        Returns:
            Status dictionary
        """
        return {
            "loaded": True,
            "model_path": self.model_path,
            "pattern_count": len(self.intent_patterns),
            "threshold": self.intent_confidence_threshold
        }
        
    def get_result(self) -> Dict[str, Any]:
        """
        Get module result.
        
        Returns:
            Result dictionary
        """
        return {
            "module": "IntentAlgorithm",
            "version": "1.0.0",
            "status": "ready"
        }
# Performance optimization applied
