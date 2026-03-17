"""
辅弼星辰 - 开放平台模块
OpenAPI规范、SDK生成、开发者生态
"""

import json
import yaml
from typing import Dict, List, Optional, Callable
from pydantic import BaseModel, Field
from enum import Enum
import hashlib
import time


class APIEndpoint(BaseModel):
    """API端点"""
    path: str
    method: str = Field(default="GET")
    summary: str = ""
    description: str = ""
    parameters: List[Dict] = Field(default_factory=list)
    request_body: Optional[Dict] = None
    responses: Dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class APISpec(BaseModel):
    """API规范"""
    title: str
    version: str = "1.0.0"
    description: str = ""
    base_url: str = ""
    endpoints: List[APIEndpoint] = Field(default_factory=list)


class Developer(BaseModel):
    """开发者"""
    developer_id: str
    name: str
    email: str
    api_keys: List[str] = Field(default_factory=list)
    tier: str = "free"  # free, basic, pro
    created_at: float = Field(default_factory=time.time)


class SDKGenerator:
    """SDK生成器"""
    
    def __init__(self):
        self.languages = ["python", "javascript", "go", "java"]
    
    def generate_python_sdk(self, spec: APISpec) -> str:
        """生成Python SDK"""
        code = f'''"""
{spec.title} - Python SDK
Version: {spec.version}
"""

import requests
from typing import Optional, Dict, Any

class {spec.title.replace(' ', '')}Client:
    """Python SDK Client"""
    
    def __init__(self, api_key: str, base_url: str = "{spec.base_url}"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({{"Authorization": f"Bearer {{api_key}}"}})
    
'''
        for endpoint in spec.endpoints:
            method_name = endpoint.path.replace('/', '_').strip('_')
            code += f'''
    def {method_name}(self{self._gen_params(endpoint.parameters)}):
        """{endpoint.summary}"""
        url = f"{{self.base_url}}{endpoint.path}"
        response = self.session.{endpoint.method.lower()}(url)
        return response.json()
'''
        return code
    
    def generate_javascript_sdk(self, spec: APISpec) -> str:
        """生成JavaScript SDK"""
        code = f'''/**
 * {spec.title} - JavaScript SDK
 * Version: {spec.version}
 */

class {spec.title.replace(' ', '')}Client {{
  constructor(apiKey, baseUrl = "{spec.base_url}") {{
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }}
  
  async request(endpoint, options = {{}}) {{
    const url = `${{this.baseUrl}}${{endpoint}}`;
    const response = await fetch(url, {{
      ...options,
      headers: {{
        ...options.headers,
        "Authorization": `Bearer ${{this.apiKey}}`
      }}
    }});
    return response.json();
  }}
'''
        for endpoint in spec.endpoints:
            method_name = endpoint.path.replace('/', '_').strip('_')
            code += f'''

  async {method_name}(params = {{}}) {{
    return this.request("{endpoint.path}", {{
      method: "{endpoint.method}",
      body: JSON.stringify(params)
    }});
  }}
'''
        code += "\n}"
        return code
    
    def _gen_params(self, parameters: List[Dict]) -> str:
        """生成参数列表"""
        if not parameters:
            return ""
        return ", " + ", ".join([p.get("name", "param") for p in parameters])


class DeveloperPortal:
    """开发者门户"""
    
    def __init__(self):
        self.developers: Dict[str, Developer] = {}
        self.api_specs: Dict[str, APISpec] = {}
        self.usage_records: List[Dict] = []
    
    def register_developer(self, name: str, email: str, tier: str = "free") -> Developer:
        """注册开发者"""
        developer_id = hashlib.md5(f"{email}{time.time()}".encode()).hexdigest()[:16]
        developer = Developer(
            developer_id=developer_id,
            name=name,
            email=email,
            tier=tier
        )
        
        # 生成API密钥
        api_key = f"xji_{developer_id}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}"
        developer.api_keys.append(api_key)
        
        self.developers[developer_id] = developer
        return developer
    
    def register_api_spec(self, spec: APISpec):
        """注册API规范"""
        self.api_specs[spec.title] = spec
    
    def get_developer(self, developer_id: str) -> Optional[Developer]:
        """获取开发者信息"""
        return self.developers.get(developer_id)
    
    def generate_api_key(self, developer_id: str) -> Optional[str]:
        """生成新的API密钥"""
        developer = self.developers.get(developer_id)
        if not developer:
            return None
        
        api_key = f"xji_{developer_id}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}"
        developer.api_keys.append(api_key)
        return api_key
    
    def record_usage(self, developer_id: str, endpoint: str, status: int):
        """记录使用情况"""
        self.usage_records.append({
            "developer_id": developer_id,
            "endpoint": endpoint,
            "status": status,
            "timestamp": time.time()
        })
    
    def get_usage_stats(self, developer_id: str) -> Dict:
        """获取使用统计"""
        records = [r for r in self.usage_records if r["developer_id"] == developer_id]
        
        return {
            "total_requests": len(records),
            "successful": len([r for r in records if r["status"] < 400]),
            "failed": len([r for r in records if r["status"] >= 400]),
            "endpoints": list(set([r["endpoint"] for r in records]))
        }


class PluginMarket:
    """插件市场"""
    
    def __init__(self):
        self.plugins: Dict[str, Dict] = {}
    
    def register_plugin(
        self,
        plugin_id: str,
        name: str,
        description: str,
        developer_id: str,
        version: str = "1.0.0"
    ):
        """注册插件"""
        self.plugins[plugin_id] = {
            "id": plugin_id,
            "name": name,
            "description": description,
            "developer_id": developer_id,
            "version": version,
            "status": "pending",  # pending, approved, rejected
            "downloads": 0,
            "rating": 0.0,
            "created_at": time.time()
        }
    
    def approve_plugin(self, plugin_id: str) -> bool:
        """审核通过插件"""
        if plugin_id in self.plugins:
            self.plugins[plugin_id]["status"] = "approved"
            return True
        return False
    
    def get_plugins(self, status: str = "approved") -> List[Dict]:
        """获取插件列表"""
        return [
            p for p in self.plugins.values()
            if p["status"] == status
        ]


# 测试代码
if __name__ == "__main__":
    # 创建API规范
    spec = APISpec(
        title="XuanJi Engine API",
        version="1.0.0",
        description="玄玑引擎开放API",
        base_url="https://api.xuanji.com/v1",
        endpoints=[
            APIEndpoint(
                path="/chat",
                method="POST",
                summary="发送消息",
                description="与AI进行对话",
                tags=["Chat"]
            ),
            APIEndpoint(
                path="/intents",
                method="GET",
                summary="获取意图列表",
                tags=["Intents"]
            )
        ]
    )
    
    # 生成SDK
    generator = SDKGenerator()
    python_code = generator.generate_python_sdk(spec)
    print("Python SDK generated:")
    print(python_code[:500])
    
    # 开发者门户
    portal = DeveloperPortal()
    dev = portal.register_developer("张三", "zhangsan@example.com")
    print(f"\n开发者注册: {dev.developer_id}")
    print(f"API Key: {dev.api_keys[0]}")
