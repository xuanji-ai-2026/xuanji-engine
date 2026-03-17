"""
玄玑引擎 - API服务入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="玄玑AI数字员工引擎 API",
    description="玄玑引擎 v0.1.0 - 十星架构MVP",
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

@app.get("/")
def root():
    return {
        "name": "玄玑AI数字员工引擎",
        "version": "0.1.0",
        "status": "running",
        "modules": {
            "紫微元灵": "意图穿透",
            "禄存星": "ReAct推理",
            "巨门星": "记忆系统",
            "武曲星": "插件系统",
            "廉贞星": "人格引擎"
        },
        "integrations": {
            "飞书机器人": "/webhook/feishu"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# 导入飞书机器人
from src.bifei.feishu_bot import create_feishu_routes
create_feishu_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
