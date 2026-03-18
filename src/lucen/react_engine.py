"""
玄玑引擎 - ReAct推理引擎（禄存星）
ReAct框架：Thought → Action → Observation → ...

作者: 玄玑引擎开发团队
日期: 2026-03-17
"""

import os
import json
from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class StepType(str, Enum):
    """推理步骤类型"""
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    ANSWER = "answer"


class ReasoningStep(BaseModel):
    """推理步骤"""
    step_type: StepType
    content: str
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    tool_name: Optional[str] = None
    tool_input: Optional[Dict] = None
    tool_output: Optional[str] = None


class ReActTrajectory(BaseModel):
    """推理轨迹"""
    user_input: str
    steps: List[ReasoningStep] = Field(default_factory=list)
    final_answer: Optional[str] = None
    success: bool = True
    reasoning_time: float = 0.0
    context: Dict[str, Any] = Field(default_factory=dict)


class Tool(BaseModel):
    """工具定义"""
    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具功能描述")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="输入参数schema")
    
    async def execute(self, **kwargs) -> str:
        """执行工具"""
        raise NotImplementedError


class ReActEngine:
    """
    ReAct推理引擎
    
    实现Thought → Action → Observation循环
    """
    
    def __init__(
        self,
        api_key: str = None,
        max_steps: int = 10,
        max_tokens: int = 4000
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        """注册默认工具"""
        # 搜索工具
        self.register_tool(SearchTool())
        # 计算工具
        self.register_tool(CalculatorTool())
        # 记忆工具
        self.register_tool(MemoryTool())
        # 天气工具
        self.register_tool(WeatherTool())
        
    def register_tool(self, tool: Tool):
        """注册工具"""
        self.tools[tool.name] = tool
        
    async def reason(
        self,
        user_input: str,
        context: Dict = None,
        tools: List[Tool] = None
    ) -> ReActTrajectory:
        """
        执行ReAct推理
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            tools: 可用工具列表
            
        Returns:
            ReActTrajectory: 推理轨迹
        """
        trajectory = ReActTrajectory(
            user_input=user_input,
            context=context or {}
        )
        
        # 合并工具
        available_tools = {**self.tools}
        if tools:
            for tool in tools:
                available_tools[tool.name] = tool
                
        # 当前状态
        current_thought = user_input
        step_count = 0
        
        # ReAct循环
        while step_count < self.max_steps:
            step_count += 1
            
            # 1. Thought: 思考下一步做什么
            thought = await self._generate_thought(
                current_thought,
                trajectory.steps,
                available_tools
            )
            
            thought_step = ReasoningStep(
                step_type=StepType.THOUGHT,
                content=thought
            )
            trajectory.steps.append(thought_step)
            
            # 检查是否需要结束
            if self._should_finish(thought):
                final_answer = await self._generate_answer(
                    current_thought,
                    trajectory.steps
                )
                trajectory.final_answer = final_answer
                trajectory.success = True
                break
                
            # 2. Action: 选择并执行工具
            action_result = await self._execute_action(
                thought,
                available_tools
            )
            
            action_step = ReasoningStep(
                step_type=StepType.ACTION,
                content=action_result["action"],
                tool_name=action_result.get("tool"),
                tool_input=action_result.get("input")
            )
            trajectory.steps.append(action_step)
            
            # 3. Observation: 观察结果
            observation_step = ReasoningStep(
                step_type=StepType.OBSERVATION,
                content=action_result["output"]
            )
            trajectory.steps.append(observation_step)
            
            # 更新当前思考
            current_thought = f"{thought}\n\n观察: {action_result['output']}"
            
        else:
            # 达到最大步数
            trajectory.final_answer = "任务复杂，已达到最大推理步数"
            trajectory.success = False
            
        return trajectory
    
    async def _generate_thought(
        self,
        current_context: str,
        steps: List[ReasoningStep],
        tools: Dict[str, Tool]
    ) -> str:
        """生成思考"""
        # 这里后续接入DeepSeek API
        # 简单模拟：检查是否需要使用工具
        available_tools_str = ", ".join([f"- {name}: {tool.description}" for name, tool in tools.items()])
        
        if "搜索" in current_context or "查" in current_context:
            return "用户需要查询信息，我应该使用搜索工具"
        elif "计算" in current_context or "算" in current_context:
            return "用户需要计算，我应该使用计算器工具"
        elif "记得" in current_context or "记忆" in current_context:
            return "用户需要回忆信息，我应该使用记忆工具"
        else:
            return "我需要分析用户意图并给出回答"
    
    def _should_finish(self, thought: str) -> bool:
        """判断是否应该结束"""
        finish_keywords = ["完成", "回答", "可以了", "就这样", "结束"]
        return any(kw in thought for kw in finish_keywords)
    
    async def _execute_action(
        self,
        thought: str,
        tools: Dict[str, Tool]
    ) -> Dict[str, Any]:
        """执行动作"""
        # 简单动作选择逻辑
        if "搜索" in thought and "搜索" in tools:
            tool = tools["搜索"]
            return {
                "action": "使用搜索工具",
                "tool": "搜索",
                "input": {"query": thought},
                "output": await tool.execute(query="测试查询结果")
            }
        elif "计算" in thought and "计算器" in tools:
            tool = tools["计算器"]
            return {
                "action": "使用计算器工具",
                "tool": "计算器",
                "input": {"expression": "1+1"},
                "output": await tool.execute(expression="1+1")
            }
        elif "记忆" in thought and "记忆" in tools:
            tool = tools["记忆"]
            return {
                "action": "使用记忆工具",
                "tool": "记忆",
                "input": {"action": "retrieve"},
                "output": await tool.execute(action="retrieve")
            }
        else:
            return {
                "action": "直接回答",
                "tool": None,
                "input": {},
                "output": "我明白了您的需求，正在处理中..."
            }
    
    async def _generate_answer(
        self,
        original_input: str,
        steps: List[ReasoningStep]
    ) -> str:
        """生成最终答案"""
        # 简单生成
        observations = [s.content for s in steps if s.step_type == StepType.OBSERVATION]
        if observations:
            return f"根据我的分析：{observations[-1]}"
        return "我理解了您的请求，正在处理。"


# ========== 内置工具 ==========

class SearchTool(Tool):
    """搜索工具"""
    name = "搜索"
    description = "搜索互联网信息"
    
    async def execute(self, query: str, **kwargs) -> str:
        return f"搜索结果：关于「{query}」的信息（模拟结果）"


class CalculatorTool(Tool):
    """计算器工具"""
    name = "计算器"
    description = "执行数学计算"
    
    async def execute(self, expression: str, **kwargs) -> str:
        try:
            # 安全计算（仅支持基本运算）
            result = eval(expression, {"__builtins__": {}}, {})
            return f"计算结果：{expression} = {result}"
        except:
            return f"无法计算表达式：{expression}"


class MemoryTool(Tool):
    """记忆工具"""
    name = "记忆"
    description = "存取长期记忆"
    
    async def execute(self, action: str = "retrieve", key: str = None, value: str = None, **kwargs) -> str:
        if action == "store":
            return f"已记住：{key} = {value}"
        elif action == "retrieve":
            return "记忆检索：未找到相关记忆（Demo）"
        return "记忆操作完成"


class WeatherTool(Tool):
    """天气工具"""
    name = "天气"
    description = "查询天气信息"
    
    async def execute(self, city: str = "北京", **kwargs) -> str:
        return f"{city}今日天气：晴，15-25°C（Demo）"


# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        engine = ReActEngine()
        
        test_cases = [
            "帮我搜索今天的新闻",
            "计算一下 123 * 456",
            "记得我的名字叫张三",
            "北京天气怎么样"
        ]
        
        for user_input in test_cases:
            print(f"\n用户输入: {user_input}")
            print("-" * 50)
            
            trajectory = await engine.reason(user_input)
            
            for step in trajectory.steps:
                print(f"[{step.step_type.value}] {step.content}")
            
            print(f"\n最终答案: {trajectory.final_answer}")
            print("=" * 50)
    
    asyncio.run(test())
