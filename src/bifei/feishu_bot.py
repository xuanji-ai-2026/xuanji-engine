"""
玄玑引擎 - 飞书机器人Webhook
"""

import hmac
import hashlib
import base64
import json
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

# 飞书配置（从环境变量读取）
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY", "")
FEISHU_VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN", "")

async def verify_feishu_signature(request: Request, body: bytes) -> bool:
    """验证飞书请求签名"""
    timestamp = request.headers.get("X-Lark-Request-Timestamp", "")
    nonce = request.headers.get("X-Lark-Request-Nonce", "")
    signature = request.headers.get("X-Lark-Signature", "")
    
    if not all([timestamp, nonce, signature, FEISHU_ENCRYPT_KEY]):
        return True  # 如果没有配置密钥，跳过验证
    
    # 计算签名
    bytes_to_sign = f"{timestamp}{nonce}{FEISHU_ENCRYPT_KEY}".encode('utf-8')
    expected_signature = base64.b64encode(
        hmac.new(FEISHU_ENCRYPT_KEY.encode(), bytes_to_sign, hashlib.sha256).digest()
    ).decode()
    
    return hmac.compare_digest(signature, expected_signature)

async def handle_feishu_event(event: dict) -> dict:
    """处理飞书事件"""
    event_type = event.get("header", {}).get("event_type", "")
    
    if event_type == "im.message.receive_v1":
        # 收到消息
        message = event.get("event", {}).get("message", {})
        content = json.loads(message.get("content", "{}"))
        user_text = content.get("text", "")
        
        # 调用玄玑引擎处理
        reply = await process_with_xuanji(user_text)
        
        # 发送回复
        await send_feishu_reply(
            message.get("chat_id"),
            reply,
            message.get("message_id")
        )
        
        return {"status": "ok"}
    
    return {"status": "ignored"}

async def process_with_xuanji(text: str) -> str:
    """调用玄玑引擎处理消息"""
    # 简单回复（后续接入完整引擎）
    responses = {
        "你好": "你好！我是玄玑AI数字员工，很高兴为你服务！",
        "help": "我可以帮你：\n1. 回答问题\n2. 执行任务\n3. 查询信息\n请告诉我你需要什么帮助",
        "帮助": "我可以帮你：\n1. 回答问题\n2. 执行任务\n3. 查询信息\n请告诉我你需要什么帮助",
    }
    
    # 关键词匹配
    for keyword, response in responses.items():
        if keyword in text:
            return response
    
    # 默认回复
    return f"收到你的消息：「{text}」\n\n我正在学习中，暂时只能处理简单对话。更多功能即将上线！"

async def send_feishu_reply(chat_id: str, text: str, parent_id: str = None):
    """发送飞书回复"""
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        print("[WARN] 飞书凭证未配置，无法发送消息")
        return
    
    try:
        # 获取tenant_access_token
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/",
                json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
            )
            token_data = token_resp.json()
            token = token_data.get("tenant_access_token", "")
            
            # 发送消息
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "receive_id": chat_id,
                "msg_type": "text",
                "content": json.dumps({"text": text})
            }
            if parent_id:
                payload["uuid"] = parent_id
            
            await client.post(
                "https://open.feishu.cn/open-apis/im/v1/messages",
                headers=headers,
                json=payload
            )
    except Exception as e:
        print(f"[ERROR] 发送飞书消息失败: {e}")

# 创建飞书路由
def create_feishu_routes(app: FastAPI):
    """创建飞书Webhook路由"""
    
    @app.post("/webhook/feishu")
    async def feishu_webhook(request: Request):
        """飞书Webhook入口"""
        body = await request.body()
        
        # 验证签名（如果配置了密钥）
        if not await verify_feishu_signature(request, body):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        data = json.loads(body)
        
        # URL验证（首次配置时需要）
        if data.get("type") == "url_verification":
            challenge = data.get("challenge", "")
            return JSONResponse({
                "challenge": challenge
            })
        
        # 处理事件
        result = await handle_feishu_event(data)
        return JSONResponse(result)
    
    @app.get("/webhook/feishu/status")
    async def feishu_status():
        """飞书机器人状态"""
        return {
            "status": "configured" if FEISHU_APP_ID else "not_configured",
            "app_id_configured": bool(FEISHU_APP_ID),
            "timestamp": datetime.now().isoformat()
        }
    
    return app
