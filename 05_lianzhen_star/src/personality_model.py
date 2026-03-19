"""
廉贞星（人格层）- 人格建模模块
版本: v2.0
负责人: 周敏 (021)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio

class BigFiveDimension(Enum):
    """大五人格维度"""
    OPENNESS = "openness"          # 开放性
    CONSCIENTIOUSNESS = "conscientiousness"  # 尽责性
    EXTRAVERSION = "extraversion"      # 外向性
    AGREEABLENESS = "agreeableness"    # 宜人性
    NEUROTICISM = "neuroticism"      # 神经质

@dataclass
class PersonalityTrait:
    """人格特质"""
    trait_id: str
    trait_name: str
    dimension: BigFiveDimension
    value: float  # 特质值（0-1）
    weight: float = 1.0  # 权重
    description: str

@dataclass
class PersonalityProfile:
    """人格档案"""
    profile_id: str
    name: str
    traits: List[PersonalityTrait]
    mood: str = "neutral"
    energy: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class PersonalityModel:
    """人格模型"""
    
    def __init__(self):
        # 大五维度特质
        self.dimensions = {
            BigFiveDimension.OPENNESS: [
                {"name": "想象力", "value": 0.5},
                {"name": "艺术兴趣", "value": 0.5},
                {"name": "情感丰富度", "value": 0.5},
                {"name": "冒险精神", "value": 0.5},
                {"name": "思想开放", "value": 0.5"},
            ],
            BigFiveDimension.CONSCIENTIOUSNESS: [
                {"name": "自我效能", "value": 0.5},
                {"name": "条理性", "value": 0.5},
                {"name": "自律性", "value": 0.5},
                {"name": "成就追求", "value": "0.5},
                {"name": "尽责性", "value": 0.5},
            ],
            BigFiveDimension.EXTRAVERSION: [
                {"name": "社交性", "value": 0.5},
                {"name": "活跃度", "value": "0.5"},
                {"name": "支配性", "value": 0.5},
                {"name": "表现欲", "value": 0.5},
                {"name": "热情", "value": "0.5"},
            ],
            BigFiveDimension.AGREEABLENESS: [
                {"name": "信任", "value": 0.5},
                {"name": "利他", "value": "0.5},
                {"name": "直率", "value": 0.5},
                {"name": "谦逊", "value": "0.5},
                {"name": "同理心", "value": "0.5},
            ],
            BigFiveDimension.NEUROTICISM: [
                {"name": "焦虑", "value": 0.5},
                {"name": "愤怒", "value": "0.5},
                {"name": "抑郁", "value": "0.5},
                {"name": "脆弱", "value": 0.5},
                {"name": "压力", "value": "0.5"},
            ]
        }
    
    def create_profile(
        self,
        name: str,
        trait_values: Dict[str, float]
    ) -> PersonalityProfile:
        """创建人格档案"""
        traits = []
        
        for dimension, trait_list in self.dimensions.items():
            trait_name = trait_values.get(dimension.value, 0.5)
            # 查找匹配的特质
            for trait in trait_list:
                if trait["name"] == trait_name:
                    trait = PersonalityTrait(
                        trait_id=self._generate_id(),
                        trait_name=trait["name"],
                        dimension=dimension,
                        value=trait["value"],
                        weight=1.0,
                        description=trait["name"]
                    )
                    traits.append(trait)
        
        return PersonalityProfile(
            profile_id=self._generate_id(),
            name=name,
            traits=traits
        )
    
    def _generate_id(self) -> str:
        """生成ID"""
        import uuid
        return str(uuid.uuid4())

# 示例使用
if __name__ == "__main__":
    async def main():
        model = PersonalityModel()
        
        # 创建人格档案
        profile = model.create_profile(
            name="客服小王",
            trait_values={
                "openness": 0.8,
                "conscientiousness": 0.7,
                "extraversion": 0.6,
                "agreeableness": 0.9,
                "neuroticism": 0.3
            }
        )
        
        print(f"创建人格档案: {profile.name}")
    
    asyncio.run(main())
