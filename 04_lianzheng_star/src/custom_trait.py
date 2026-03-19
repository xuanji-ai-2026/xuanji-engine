"""
廉贞星（人格层）- 人格建模
版本: v2.0
负责人: 余廉心 (164)
功能: 自定义特质系统
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import asyncio

@dataclass
class CustomTrait:
    """自定义特质"""
    trait_id: str
    name: str
    category: str
    min_value: float = 0.0
    max_value: float = 1.0
    default_value: float = 0.5

class CustomTraitSystem:
    """自定义特质系统"""
    
    def __init__(self):
        self.traits: Dict[str, CustomTrait] = {}
        self._init_default_traits()
    
    def _init_default_traits(self):
        """初始化默认特质"""
        default_traits = [
            {"name": "幽默感", "category": "性格", "min": 0.0, "max": 1.0},
            {"name": "耐心", "category": "性格", "min": 0.0, "max": 1.0},
            {"name": "创造力", "category": "能力", "min": 0.0, "max": 1.0},
            {"name": "同理心", "category": "情感", "min": 0.0, "max": 1.0},
            {"name": "逻辑思维", "category": "能力", "min": 0.0, "max": 1.0},
        ]
        # ... 共100+特质
    
    async def add_trait(self, trait: CustomTrait):
        """添加特质"""
        self.traits[trait.trait_id] = trait
    
    async def get_trait(self, trait_id: str) -> Optional[CustomTrait]:
        """获取特质"""
        return self.traits.get(trait_id)

__all__ = ["CustomTrait", "CustomTraitSystem"]
