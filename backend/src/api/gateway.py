"""
玄玑引擎 - API网关（DeepSeek集成版）
支持外部系统调用
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import time
import httpx

app = FastAPI(
    title="玄玑AI数字员工引擎 API Gateway",
    description="统一API入口，支持外部系统调用",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DeepSeek配置 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-493d37873df8461780f9f02074ef1862")

async def call_deepseek(prompt: str, context: str = "") -> str:
    """调用DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建消息
    system_prompt = """你是一个专业的AI数字员工助手，名叫"玄玑"。
你能够回答用户的问题，执行任务，提供帮助。
请用友好、专业的方式回复。"""
    
    if context:
        system_prompt += f"\n\n上下文信息：{context}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"抱歉，我现在无法回答您的问题。请稍后再试。\n\n(错误: {str(e)[:50]})"

# ========== 认证 ==========
API_KEYS = {
    "xuanji-default": {"name": "默认密钥", "tier": "free"},
    "xuanji-pro": {"name": "专业版", "tier": "pro"},
}

def verify_api_key(x_api_key: Optional[str] = Header(None)) -> Dict:
    """验证API密钥"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="缺少API密钥")
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="无效的API密钥")
    return API_KEYS[x_api_key]

# ========== 请求模型 ==========
class ChatRequest(BaseModel):
    """对话请求"""
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class IntentRequest(BaseModel):
    """意图识别请求"""
    text: str

class ReActRequest(BaseModel):
    """推理请求"""
    user_input: str

# ========== API端点 ==========

@app.get("/")
def root():
    return {
        "name": "玄玑AI数字员工引擎 API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "ai_model": "deepseek-chat",
        "endpoints": {
            "chat": "/api/v1/chat",
            "intent": "/api/v1/intent",
            "react": "/api/v1/react",
            "status": "/api/v1/status"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# ========== 对话接口 ==========

@app.post("/api/v1/chat")
async def chat(request: ChatRequest, auth: Dict = Depends(verify_api_key)):
    """
    对话接口 - 外部系统调用入口
    
    使用方式：
    ```
    curl -X POST http://xuanji.kuncantech.com/api/v1/chat \
      -H "Content-Type: application/json" \
      -H "X-API-Key: xuanji-default" \
      -d '{"message": "你好", "user_id": "user001"}'
    ```
    """
    # 调用DeepSeek API
    reply = await call_deepseek(request.message, str(request.context or ""))
    
    return {
        "code": 0,
        "message": "success",
        "data": {
            "reply": reply,
            "intent": "deepseek",
            "message_id": f"msg_{int(time.time())}"
        }
    }

@app.post("/api/v1/chat/simple")
async def simple_chat(message: str):
    """简化的对话接口（无需认证）"""
    reply = await call_deepseek(message)
    return {
        "code": 0,
        "data": {"reply": reply}
    }

@app.post("/api/v1/intent")
async def intent(request: IntentRequest, auth: Dict = Depends(verify_api_key)):
    """意图识别接口"""
    # 使用DeepSeek进行意图识别
    prompt = f"""请识别用户意图，只返回意图类型。
用户消息：{request.text}

意图类型选项：
- greeting: 问候
- help: 请求帮助
- query: 查询信息
- task: 执行任务
- chat: 闲聊
- other: 其他

只返回意图类型名称，不要其他内容。"""
    
    intent_type = await call_deepseek(prompt)
    intent_type = intent_type.strip().lower()
    
    return {
        "code": 0,
        "data": {
            "intent": intent_type,
            "text": request.text
        }
    }

@app.post("/api/v1/react")
async def react(request: ReActRequest, auth: Dict = Depends(verify_api_key)):
    """ReAct推理接口"""
    # 使用DeepSeek进行推理
    prompt = f"""请分析并回答用户问题，展示你的思考过程。
    
用户输入：{request.user_input}

请按照以下格式回答：
1. 思考：...
2. 行动：...
3. 回答：..."""
    
    result = await call_deepseek(prompt)
    
    return {
        "code": 0,
        "data": {
            "result": result,
            "intent": "react"
        }
    }

@app.get("/api/v1/status")
async def api_status(auth: Dict = Depends(verify_api_key)):
    """API状态"""
    return {
        "code": 0,
        "data": {
            "tier": auth["tier"],
            "tier_name": auth["name"],
            "engine_version": "0.1.0",
            "ai_model": "deepseek-chat",
            "api_key_configured": bool(DEEPSEEK_API_KEY)
        }
    }

@app.get("/api/v1/keys")
async def list_keys():
    """列出可用密钥"""
    return {
        "keys": [
            {"key": k, "name": v["name"], "tier": v["tier"]}
            for k, v in API_KEYS.items()
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
