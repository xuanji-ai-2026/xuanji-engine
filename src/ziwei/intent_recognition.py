"""
玄玑引擎 - 意图识别模块（紫微元灵）
意图穿透：理解用户深层需求

作者: 玄玑引擎开发团队
日期: 2026-03-17
"""

import os
import json
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum


class IntentType(str, Enum):
    """意图类型枚举"""
    CREATE_DIGITAL_HUMAN = "创建数字人"
    TASK_EXECUTION = "任务执行"
    INFORMATION_QUERY = "信息查询"
    EMOTIONAL_EXCHANGE = "情感交流"
    CONFIG_MANAGEMENT = "配置管理"
    SKILL_TRAINING = "技能训练"
    DATA_ANALYSIS = "数据分析"
    SCHEDULE_MANAGEMENT = "日程管理"
    COMMUNICATION = "通讯联络"
    SYSTEM_CONTROL = "系统控制"


class Intent(BaseModel):
    """意图模型"""
    intent_type: IntentType = Field(..., description="意图类型")
    confidence: float = Field(..., ge=0, le=1, description="置信度")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="意图参数")
    reasoning: Optional[str] = Field(None, description="推理过程")
    sub_intents: List[str] = Field(default_factory=list, description="子意图")


class IntentRecognizer:
    """
    意图识别器
    
    使用DeepSeek API进行多模态意图识别
    """
    
    # 意图关键词映射
    INTENT_KEYWORDS = {
        IntentType.CREATE_DIGITAL_HUMAN: [
            "创建数字人", "做一个数字人", "生成数字人", "数字人",
            "AI员工", "虚拟员工", "数字员工"
        ],
        IntentType.TASK_EXECUTION: [
            "帮我", "执行", "完成", "做一下", "处理"
        ],
        IntentType.INFORMATION_QUERY: [
            "查询", "搜索", "找一下", "看看", "什么是"
        ],
        IntentType.EMOTIONAL_EXCHANGE: [
            "聊天", "说话", "聊聊", "心情", "情感"
        ],
        IntentType.DATA_ANALYSIS: [
            "分析", "统计", "报表", "数据"
        ],
        IntentType.SCHEDULE_MANAGEMENT: [
            "日程", "会议", "安排", "预约"
        ],
        IntentType.COMMUNICATION: [
            "发邮件", "打电话", "发消息", "通知"
        ],
    }
    
    def __init__(self, api_key: str = None):
        """
        初始化意图识别器
        
        Args:
            api_key: DeepSeek API Key
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com"
        
    async def recognize(self, text: str, context: Dict = None) -> Intent:
        """
        识别文本意图
        
        Args:
            text: 用户输入文本
            context: 上下文信息（可选）
            
        Returns:
            Intent: 意图对象
        """
        # 1. 关键词匹配（快速路径）
        keyword_intent = self._keyword_match(text)
        if keyword_intent:
            return keyword_intent
        
        # 2. LLM推理（精确路径）
        llm_intent = await self._llm_recognize(text, context)
        return llm_intent
    
    def _keyword_match(self, text: str) -> Optional[Intent]:
        """关键词匹配"""
        for intent_type, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return Intent(
                        intent_type=intent_type,
                        confidence=0.8,
                        parameters={"keyword": keyword},
                        reasoning=f"关键词匹配: {keyword}"
                    )
        return None
    
    async def _llm_recognize(self, text: str, context: Dict = None) -> Intent:
        """使用LLM进行意图识别"""
        # 这里后续接入DeepSeek API
        # 暂时返回默认意图
        return Intent(
            intent_type=IntentType.TASK_EXECUTION,
            confidence=0.5,
            parameters={"text": text},
            reasoning="默认意图（LLM待接入）"
        )
    
    async def recognize_batch(self, texts: List[str]) -> List[Intent]:
        """批量识别意图"""
        return [await self.recognize(text) for text in texts]


# 意图管理器 - 管理和协调多个意图识别器
class IntentManager:
    """意图管理器"""
    
    def __init__(self, api_key: str = None):
        self.recognizer = IntentRecognizer(api_key)
        
    async def recognize(self, text: str, context: Dict = None) -> Intent:
        """识别意图"""
        return await self.recognizer.recognize(text, context)
    
    def extract_entities(self, text: str, intent: Intent) -> Dict[str, Any]:
        """从文本中提取实体"""
        entities = {}
        
        # 提取人名
        if "给" in text and "发" in text:
            # 尝试提取收件人
            parts = text.split("给")
            if len(parts) > 1:
                entities["recipient"] = parts[1].split()[0]
                
        # 提取时间
        time_keywords = ["今天", "明天", "后天", "上午", "下午", "晚上", "点"]
        for keyword in time_keywords:
            if keyword in text:
                entities["time"] = keyword
                break
                
        return entities


# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        manager = IntentManager()
        
        test_cases = [
            "帮我创建一个电话销售数字人",
            "查询张三的联系方式",
            "分析Q1销售数据",
            "明天上午10点开会",
            "给李总发邮件"
        ]
        
        for text in test_cases:
            intent = await manager.recognize(text)
            print(f"文本: {text}")
            print(f"意图: {intent.intent_type.value}")
            print(f"置信度: {intent.confidence}")
            print(f"推理: {intent.reasoning}")
            print("-" * 50)
    
    asyncio.run(test())
