"""
Personality Engine Module
Author: 元廉情 (Employee ID: 165)
Group: XJ-04 廉贞星
Task: 人格引擎实现
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class PersonalityType(Enum):
    """Personality types."""
    OPEN = "open"
    CONSERVATIVE = "conservative"
    EXTROVERT = "extrovert"
    INTROVERT = "introvert"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"


@dataclass
class PersonalityProfile:
    """Personality profile."""
    openness: float  # 0-1
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float


class PersonalityEngine:
    """Personality Engine Implementation"""
    
    def __init__(self):
        """Initialize the personality engine."""
        self.profiles: Dict[str, PersonalityProfile] = {}
        
    def create_profile(
        self,
        user_id: str,
        openness: float = 0.5,
        conscientiousness: float = 0.5,
        extraversion: float = 0.5,
        agreeableness: float = 0.5,
        neuroticism: float = 0.5
    ) -> PersonalityProfile:
        """
        Create a personality profile.
        
        Args:
            user_id: User ID
            openness: Openness score
            conscientiousness: Conscientiousness score
            extraversion: Extraversion score
            agreeableness: Agreeableness score
            neuroticism: Neuroticism score
            
        Returns:
            PersonalityProfile instance
        """
        profile = PersonalityProfile(
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism
        )
        
        self.profiles[user_id] = profile
        return profile
        
    def get_profile(self, user_id: str) -> PersonalityProfile:
        """Get user personality profile."""
        if user_id not in self.profiles:
            # Return default profile
            return self.create_profile(user_id)
        return self.profiles[user_id]
        
    def get_dominant_traits(self, profile: PersonalityProfile) -> List[str]:
        """Get dominant personality traits."""
        traits = [
            ("openness", profile.openness),
            ("conscientiousness", profile.conscientiousness),
            ("extraversion", profile.extraversion),
            ("agreeableness", profile.agreeableness),
            ("neuroticism", profile.neuroticism)
        ]
        
        # Sort by score
        sorted_traits = sorted(traits, key=lambda x: x[1], reverse=True)
        
        return [trait[0] for trait in sorted_traits[:3]]
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "profiles_count": len(self.profiles)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "PersonalityEngine",
            "version": "1.0.0",
            "status": "ready"
        }
