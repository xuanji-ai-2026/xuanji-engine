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
        self.empathy_model = EmpathyModel()
        
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
    
    def analyze_user_emotion(self, text: str) -> EmotionState:
        """分析用户情绪"""
        # 简化实现：基于关键词检测
        keywords = {
            EmotionState.HAPPY: ["开心", "高兴", "快乐", "满意", "喜欢"],
            EmotionState.SAD: ["难过", "伤心", "悲伤", "痛苦", "失望"],
            EmotionState.ANGRY: ["生气", "愤怒", "烦", "讨厌", "不满"],
            EmotionState.FEAR: ["害怕", "担心", "紧张", "恐惧", "焦虑"],
            EmotionState.SURPRISE: ["惊讶", "意外", "震惊", "不可思议"],
            EmotionState.NEUTRAL: ["好的", "收到", "明白", "可以", "了解"]
        }
        
        for emotion, words in keywords.items():
            for word in words:
                if word in text:
                    return emotion
        
        return EmotionState.NEUTRAL


class EmpathyModel(BaseModel):
    """共情模型 - 理解并回应用户情绪"""
    
    def __init__(self):
        self.emotion_keywords = {
            "positive": ["好", "棒", "优秀", "厉害", "开心", "高兴", "喜欢", "满意", "不错"],
            "negative": ["不好", "差", "糟", "烦", "生气", "讨厌", "失望", "痛苦", "难过"],
            "neutral": ["好的", "收到", "明白", "可以", "了解", "嗯", "哦"]
        }
        
        self.empathy_responses = {
            EmotionState.HAPPY: [
                "太好了！听到你这么开心我也很愉快！",
                "这个消息真不错！继续保持！",
                "我很高兴能帮到你！"
            ],
            EmotionState.SAD: [
                "我理解你现在的感受，如果需要倾诉我随时在这里。",
                "这确实让人难过，不过我相信你能度过难关。",
                "别担心，一切都会好起来的。"
            ],
            EmotionState.ANGRY: [
                "我理解你的不满，让我们一起看看如何解决。",
                "这种情况确实令人沮丧，冷静一下我们慢慢处理。",
                "我明白你的感受，让我们一起想办法。"
            ],
            EmotionState.FEAR: [
                "别担心，有我在这里陪着你。",
                "这种情况虽然让人紧张，但我们会一起面对。",
                "深呼吸，一步步来，没问题的。"
            ],
            EmotionState.SURPRISE: [
                "这确实让人意外！让我们仔细看看。",
                "哇，这很有意思！",
                "我也没想到会是这样的结果。"
            ],
            EmotionState.NEUTRAL: [
                "好的，我明白了。",
                "收到，继续吧。",
                "了解了，有什么我可以帮你的？"
            ]
        }
    
    def detect_emotion(self, text: str) -> EmotionState:
        """检测文本中的情绪"""
        for emotion, keywords in self.emotion_keywords.items():
            if isinstance(emotion, str):
                # 对于简单的字符串key，暂时映射
                pass
        
        # 基于关键词检测
        lower_text = text.lower()
        if any(word in lower_text for word in self.emotion_keywords["positive"]):
            return EmotionState.HAPPY
        elif any(word in lower_text for word in self.emotion_keywords["negative"]):
            return EmotionState.SAD
        elif any(word in lower_text for word in self.emotion_keywords["neutral"]):
            return EmotionState.NEUTRAL
        
        return EmotionState.NEUTRAL
    
    def generate_empathetic_response(
        self,
        emotion: EmotionState,
        context: str = ""
    ) -> str:
        """生成共情回复"""
        responses = self.empathy_responses.get(emotion, [])
        
        if not responses:
            return "我理解你的感受。"
        
        # 根据上下文选择最合适的回复
        import random
        return random.choice(responses)
    
    def analyze_emotion_intensity(self, text: str) -> float:
        """分析情绪强度（0.0-1.0）"""
        # 简化实现：基于标点和特殊符号
        intensity_indicators = ["!", "！", "~~~", "...", "???", "!!!"]
        count = sum(1 for indicator in intensity_indicators if indicator in text)
        return min(1.0, count * 0.3)
    
    def should_apply_empathy(self, persona_config: PersonaConfig) -> bool:
        """判断是否应该应用共情"""
        if not persona_config:
            return False
        return persona_config.empathy_enabled


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
