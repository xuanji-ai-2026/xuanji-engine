"""
廉贞星 - 人格引擎模块
人格配置、情绪状态、共情模型
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import yaml
import os


class EmotionState(str, Enum):
    """情绪状态"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEAR = "fear"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"


class PersonalityTrait(BaseModel):
    """人格特质"""
    openness: float = Field(default=0.5, ge=0, le=1)  # 开放性
    conscientiousness: float = Field(default=0.5, ge=0, le=1)  # 责任心
    extraversion: float = Field(default=0.5, ge=0, le=1)  # 外向性
    agreeableness: float = Field(default=0.5, ge=0, le=1)  # 宜人性
    neuroticism: float = Field(default=0.5, ge=0, le=1)  # 神经质


class PersonaConfig(BaseModel):
    """人格配置"""
    name: str = Field(default="default")
    description: str = Field(default="")
    traits: PersonalityTrait = Field(default_factory=PersonalityTrait)
    default_emotion: EmotionState = Field(default=EmotionState.NEUTRAL)
    emotion_decay: float = Field(default=0.1)  # 情绪衰减速度
    empathy_enabled: bool = Field(default=True)  # 共情能力


class EmotionEngine(BaseModel):
    """情绪引擎"""
    current_emotion: EmotionState = Field(default=EmotionState.NEUTRAL)
    emotion_intensity: float = Field(default=0.5, ge=0, le=1)
    emotion_history: List[Dict] = Field(default_factory=list)
    
    def update_emotion(self, new_emotion: EmotionState, intensity: float = 0.5):
        """更新情绪"""
        self.current_emotion = new_emotion
        self.emotion_intensity = intensity
        self.emotion_history.append({
            "emotion": new_emotion.value,
            "intensity": intensity
        })
    
    def decay_emotion(self):
        """情绪衰减"""
        self.emotion_intensity = max(0, self.emotion_intensity - 0.1)


class PersonalityEngine:
    """人格引擎"""
    
    def __init__(self, config_path: str = None):
        self.configs: Dict[str, PersonaConfig] = {}
        self.active_persona: Optional[PersonaConfig] = None
        self.emotion_engine = EmotionEngine()
        
        # 加载默认配置
        if config_path and os.path.exists(config_path):
            self.load_configs(config_path)
        else:
            self._init_default_configs()
    
    def _init_default_configs(self):
        """初始化默认人格配置"""
        # 助手型
        self.configs["assistant"] = PersonaConfig(
            name="assistant",
            description="专业、友好、有耐心",
            traits=PersonalityTrait(
                openness=0.7,
                conscientiousness=0.9,
                extraversion=0.6,
                agreeableness=0.9,
                neuroticism=0.2
            ),
            default_emotion=EmotionState.NEUTRAL,
            empathy_enabled=True
        )
        
        # 创意型
        self.configs["creative"] = PersonaConfig(
            name="creative",
            description="有想象力、善于创新",
            traits=PersonalityTrait(
                openness=0.9,
                conscientiousness=0.6,
                extraversion=0.7,
                agreeableness=0.6,
                neuroticism=0.4
            ),
            default_emotion=EmotionState.HAPPY,
            empathy_enabled=True
        )
        
        # 理性型
        self.configs["analytical"] = PersonaConfig(
            name="analytical",
            description="逻辑性强、客观冷静",
            traits=PersonalityTrait(
                openness=0.8,
                conscientiousness=0.9,
                extraversion=0.3,
                agreeableness=0.5,
                neuroticism=0.2
            ),
            default_emotion=EmotionState.NEUTRAL,
            empathy_enabled=False
        )
    
    def load_configs(self, config_path: str):
        """加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            for name, config in data.items():
                self.configs[name] = PersonaConfig(**config)
    
    def set_persona(self, name: str) -> bool:
        """设置人格"""
        if name in self.configs:
            self.active_persona = self.configs[name]
            return True
        return False
    
    def get_response_style(self, emotion: EmotionState = None) -> Dict:
        """获取回复风格"""
        if not self.active_persona:
            return {"tone": "neutral", "empathy": False}
        
        emotion = emotion or self.emotion_engine.current_emotion
        
        style_map = {
            EmotionState.HAPPY: {"tone": "joyful", "empathy": True},
            EmotionState.SAD: {"tone": "sympathetic", "empathy": True},
            EmotionState.ANGRY: {"tone": "calm", "empathy": True},
            EmotionState.FEAR: {"tone": "reassuring", "empathy": True},
            EmotionState.SURPRISE: {"tone": "curious", "empathy": True},
            EmotionState.NEUTRAL: {"tone": "neutral", "empathy": self.active_persona.empathy_enabled}
        }
        
        return style_map.get(emotion, style_map[EmotionState.NEUTRAL])


# 测试代码
if __name__ == "__main__":
    engine = PersonalityEngine()
    
    print("可用人格配置:", list(engine.configs.keys()))
    
    # 设置助手人格
    engine.set_persona("assistant")
    print("\n当前人格:", engine.active_persona.name)
    print("回复风格:", engine.get_response_style())
    
    # 更新情绪
    engine.emotion_engine.update_emotion(EmotionState.HAPPY, 0.8)
    print("情绪更新后:", engine.get_response_style(EmotionState.HAPPY))
