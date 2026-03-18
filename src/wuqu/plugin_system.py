"""
玄玑引擎 - 插件系统（武曲星）
标准化插件接口与生命周期管理

作者: 玄玑引擎开发团队
日期: 2026-03-17
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import asyncio


class RiskLevel(str, Enum):
    """风险等级"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PluginResult(BaseModel):
    """插件执行结果"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0


class BasePlugin(ABC):
    """
    插件基类
    
    所有插件必须继承此类并实现execute方法
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """插件唯一标识"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """插件功能描述"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass
    
    @property
    def risk_level(self) -> RiskLevel:
        """风险等级"""
        return RiskLevel.LOW
    
    @property
    def schema(self) -> Dict:
        """输入输出Schema"""
        return {}
    
    @property
    def permissions(self) -> List[str]:
        """所需权限"""
        return []
    
    @abstractmethod
    async def execute(self, context: Any, params: Dict) -> PluginResult:
        """执行插件逻辑"""
        pass
    
    async def validate(self, params: Dict) -> tuple[bool, Optional[str]]:
        """参数校验"""
        return True, None


class PluginRegistry:
    """
    插件注册中心
    管理所有可用插件
    """
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        
    def register(self, plugin: BasePlugin):
        """注册插件"""
        self.plugins[plugin.name] = plugin
        
    def unregister(self, name: str):
        """注销插件"""
        if name in self.plugins:
            del self.plugins[name]
            
    def get(self, name: str) -> Optional[BasePlugin]:
        """获取插件"""
        return self.plugins.get(name)
    
    def list_all(self) -> List[BasePlugin]:
        """列出所有插件"""
        return list(self.plugins.values())
    
    def search(self, keyword: str) -> List[BasePlugin]:
        """搜索插件"""
        return [
            p for p in self.plugins.values()
            if keyword.lower() in p.name.lower()
            or keyword.lower() in p.description.lower()
        ]


# ========== 内置插件 ==========

class CalculatorPlugin(BasePlugin):
    """计算器插件"""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "数学计算器，支持加减乘除"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def risk_level(self) -> RiskLevel:
        return RiskLevel.LOW
    
    @property
    def schema(self) -> Dict:
        return {
            "expression": {"type": "string", "required": True}
        }
    
    async def execute(self, context: Any, params: Dict) -> PluginResult:
        expression = params.get("expression", "")
        
        try:
            # 安全计算
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return PluginResult(
                    success=False,
                    error="包含非法字符"
                )
                
            result = eval(expression, {"__builtins__": {}}, {})
            return PluginResult(success=True, data=str(result))
            
        except Exception as e:
            return PluginResult(success=False, error=str(e))


class SearchPlugin(BasePlugin):
    """搜索插件"""
    
    @property
    def name(self) -> str:
        return "search"
    
    @property
    def description(self) -> str:
        return "互联网搜索"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def risk_level(self) -> RiskLevel:
        return RiskLevel.MEDIUM
    
    async def execute(self, context: Any, params: Dict) -> PluginResult:
        query = params.get("query", "")
        
        # 模拟搜索结果
        results = [
            {"title": f"关于{query}的结果1", "url": "https://example.com/1"},
            {"title": f"关于{query}的结果2", "url": "https://example.com/2"},
        ]
        
        return PluginResult(success=True, data=results)


class EmailPlugin(BasePlugin):
    """邮件发送插件"""
    
    @property
    def name(self) -> str:
        return "email"
    
    @property
    def description(self) -> str:
        return "发送电子邮件"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def risk_level(self) -> RiskLevel:
        return RiskLevel.HIGH
    
    @property
    def permissions(self) -> List[str]:
        return ["email:send"]
    
    async def execute(self, context: Any, params: Dict) -> PluginResult:
        to = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")
        
        # 模拟发送
        return PluginResult(
            success=True,
            data={
                "message_id": "msg_123456",
                "to": to,
                "subject": subject
            }
        )


# 注册默认插件
def get_default_registry() -> PluginRegistry:
    registry = PluginRegistry()
    registry.register(CalculatorPlugin())
    registry.register(SearchPlugin())
    registry.register(EmailPlugin())
    return registry


# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        registry = get_default_registry()
        
        # 列出所有插件
        print("可用插件:")
        for plugin in registry.list_all():
            print(f"- {plugin.name}: {plugin.description} (v{plugin.version})")
        
        # 执行计算器插件
        calc = registry.get("calculator")
        result = await calc.execute(None, {"expression": "1+2*3"})
        print(f"\n计算结果: {result.data}")
        
        # 执行搜索插件
        search = registry.get("search")
        result = await search.execute(None, {"query": "AI"})
        print(f"\n搜索结果: {result.data}")
    
    asyncio.run(test())
