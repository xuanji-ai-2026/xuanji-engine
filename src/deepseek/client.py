"""
玄玑引擎 - DeepSeek API集成
智能对话能力
"""

import os
import httpx
from typing import Dict, Optional

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-493d37873df8461780f9f02074ef1862")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

class DeepSeekClient:
    """DeepSeek API 客户端"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
        self.model = "deepseek-chat"
        
    async def chat(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict:
        """发送对话请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": str(e)}
    
    async def simple_chat(self, prompt: str) -> str:
        """简单对话"""
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages)
        
        if "error" in result:
            return f"API错误: {result['error']}"
        
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "解析响应失败"


# 全局实例
deepseek_client = DeepSeekClient()

# 测试
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("测试DeepSeek API...")
        response = await deepseek_client.simple_chat("你好，请介绍一下你自己")
        print(f"回复: {response}")
    
    asyncio.run(test())
