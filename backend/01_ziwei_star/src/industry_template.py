"""
紫微帝星（元灵层）- 行业数字人模板引擎
版本: v2.0
负责人: 赵四维 (109)
功能: 22+行业模板一键生成数字人
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

class IndustryType(Enum):
    """行业类型"""
    MEDICAL = "medical"           # 医疗健康
    EDUCATION = "education"        # 教育培训
    FINANCE = "finance"           # 金融保险
    GOVERNMENT = "government"     # 政务管理
    LEGAL = "legal"               # 法律咨询
    ECOMMERCE = "ecommerce"       # 电商客服
    HOTEL = "hotel"              # 酒店旅游
    HEALTH = "health"             # 健康管理
    REALESTATE = "realestate"     # 房地产
    AUTOMOTIVE = "automotive"     # 汽车服务
    # ... 共22+行业

@dataclass
class IndustryTemplate:
    """行业模板"""
    template_id: str
    industry: IndustryType
    name: str
    description: str
    default_personality: Dict[str, float]  # Big Five人格
    default_skills: List[str]
    knowledge_domains: List[str]
    response_style: str
    language_support: List[str]

class TemplateEngine:
    """模板引擎"""
    
    def __init__(self):
        self.templates: Dict[str, IndustryTemplate] = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """初始化行业模板"""
        self.templates = {
            "medical": IndustryTemplate(
                template_id="medical_001",
                industry=IndustryType.MEDICAL,
                name="医疗健康顾问",
                description="专业医疗健康咨询数字人",
                default_personality={
                    "openness": 0.8,
                    "conscientiousness": 0.9,
                    "extraversion": 0.6,
                    "agreeableness": 0.9,
                    "neuroticism": 0.3
                },
                default_skills=["健康咨询", "疾病预防", "用药指导"],
                knowledge_domains=["医学", "药学", "护理"],
                response_style="专业、温和、耐心",
                language_support=["中文", "英文"]
            ),
            "education": IndustryTemplate(
                template_id="education_001",
                industry=IndustryType.EDUCATION,
                name="教育培训导师",
                description="专业教育培训数字人",
                default_personality={
                    "openness": 0.9,
                    "conscientiousness": 0.9,
                    "extraversion": 0.7,
                    "agreeableness": 0.8,
                    "neuroticism": 0.2
                },
                default_skills=["知识讲解", "答疑解惑", "作业辅导"],
                knowledge_domains=["K12", "高等教育", "职业教育"],
                response_style="专业、活泼、鼓励",
                language_support=["中文", "英文"]
            ),
            "finance": IndustryTemplate(
                template_id="finance_001",
                industry=IndustryType.FINANCE,
                name="金融保险顾问",
                description="专业金融保险咨询数字人",
                default_personality={
                    "openness": 0.7,
                    "conscientiousness": 0.9,
                    "extraversion": 0.5,
                    "agreeableness": 0.7,
                    "neuroticism": 0.3
                },
                default_skills=["理财咨询", "保险规划", "投资分析"],
                knowledge_domains=["金融", "保险", "投资"],
                response_style="专业、严谨、稳重",
                language_support=["中文", "英文"]
            ),
            # ... 更多模板
        }
    
    async def create_digital_human(
        self,
        template_id: str,
        custom_settings: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """创建数字人"""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # 合并默认设置和自定义设置
        settings = {
            "personality": template.default_personality.copy(),
            "skills": template.default_skills.copy(),
            "knowledge_domains": template.knowledge_domains.copy(),
            "response_style": template.response_style,
            "language_support": template.language_support
        }
        
        if custom_settings:
            settings.update(custom_settings)
        
        return {
            "digital_human_id": self._generate_id(),
            "template": template.name,
            "settings": settings
        }
    
    async def list_templates(self) -> List[IndustryTemplate]:
        """列出所有模板"""
        return list(self.templates.values())
    
    async def get_template(self, template_id: str) -> Optional[IndustryTemplate]:
        """获取模板"""
        return self.templates.get(template_id)
    
    def _generate_id(self) -> str:
        import uuid
        return f"dh_{uuid.uuid4().hex[:8]}"

class KnowledgeInjector:
    """知识注入系统"""
    
    def __init__(self):
        self.knowledge_base = {}
    
    async def inject_knowledge(
        self,
        digital_human_id: str,
        knowledge: Dict[str, Any]
    ):
        """注入知识"""
        if digital_human_id not in self.knowledge_base:
            self.knowledge_base[digital_human_id] = []
        
        self.knowledge_base[digital_human_id].append(knowledge)
    
    async def get_knowledge(
        self,
        digital_human_id: str
    ) -> List[Dict]:
        """获取知识"""
        return self.knowledge_base.get(digital_human_id, [])

# 导出
__all__ = ["IndustryType", "IndustryTemplate", "TemplateEngine", "KnowledgeInjector"]
