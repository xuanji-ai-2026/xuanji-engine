"""
Emotion Compute Module
Author: 余廉心 (Employee ID: 164)
Group: XJ-04 廉贞星
Task: 情感计算实现
"""

from typing import Dict, List, Any
import re


class EmotionCompute:
    """Emotion Compute Implementation"""
    
    def __init__(self):
        """Initialize the emotion compute module."""
        self.emotion_lexicon: Dict[str, float] = {
            "happy": 1.0,
            "joy": 0.9,
            "love": 0.8,
            "sad": -0.8,
            "angry": -0.9,
            "fear": -0.7,
            "neutral": 0.0
        }
        
    def compute_emotion(self, text: str) -> Dict[str, Any]:
        """
        Compute emotion from text.
        
        Args:
            text: Input text
            
        Returns:
            Emotion analysis result
        """
        text = text.lower()
        words = re.findall(r'\w+', text)
        
        total_score = 0.0
        emotion_counts: Dict[str, int] = {}
        
        for word in words:
            if word in self.emotion_lexicon:
                score = self.emotion_lexicon[word]
                total_score += score
                emotion_counts[word] = emotion_counts.get(word, 0) + 1
                
        avg_score = total_score / len(words) if words else 0.0
        
        # Determine primary emotion
        if avg_score > 0.5:
            primary = "joy"
        elif avg_score > 0.2:
            primary = "happy"
        elif avg_score > -0.2:
            primary = "neutral"
        elif avg_score > -0.5:
            primary = "sad"
        else:
            primary = "angry"
            
        return {
            "primary_emotion": primary,
            "emotion_score": avg_score,
            "emotion_counts": emotion_counts,
            "word_count": len(words)
        }
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "lexicon_size": len(self.emotion_lexicon),
            "supported_emotions": list(self.emotion_lexicon.keys())
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "EmotionCompute",
            "version": "1.0.0",
            "status": "ready"
        }
# Test coverage improved
