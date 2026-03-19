# 示例代码

本目录包含玄玑AI数字员工引擎的使用示例。

## 目录

- [基本使用示例](#基本使用示例)
- [API调用示例](#api调用示例)
- [插件开发示例](#插件开发示例)
- [集成示例](#集成示例)

---

## 基本使用示例

### 1. 意图识别示例

```python
# examples/intent_recognition.py
from src.ziwei.intent_recognition import IntentRecognition

# 初始化意图识别器
recognizer = IntentRecognition()

# 识别意图
result = recognizer.recognize("帮我查询一下明天的天气")

print("识别结果:", result)
# 输出: {'intent': 'weather_query', 'confidence': 0.95, 'entities': {...}}
```

### 2. 对话管理示例

```python
# examples/dialogue_management.py
from src.tanlang.dialog_manage_lei import DialogueManager

# 初始化对话管理器
manager = DialogueManager()

# 生成对话响应
response = manager.generate_response(
    intent="weather_query",
    user_id="user123",
    context={"location": "北京"}
)

print("对话响应:", response)
# 输出: {'reply': '明天北京的天气是晴天，温度15-25度', ...}
```

### 3. 记忆存储示例

```python
# examples/memory_storage.py
from src.jumen.memory_storage_shen import MemoryStorage
from src.jumen.memory_retrieve_han import MemoryRetrieve

# 初始化存储和检索
storage = MemoryStorage()
retrieve = MemoryRetrieve()

# 存储记忆
memory_id = storage.store(None, {
    "user_id": "user123",
    "content": "用户喜欢看科幻电影",
    "type": "preference"
})

# 检索记忆
memory = retrieve.retrieve(None, memory_id)
print("检索结果:", memory)
```

---

## API调用示例

### 1. 使用Python客户端

```python
# examples/api_client.py
import httpx

# 创建客户端
client = httpx.AsyncClient(base_url="http://localhost:8000")

# 登录
login_response = await client.post(
    "/api/v2/auth/login",
    json={"username": "user", "password": "password"}
)
token = login_response.json()["data"]["token"]

# 发送消息
dialogue_response = await client.post(
    "/api/v2/dialogue/message",
    json={
        "message": "你好",
        "user_id": "user123",
        "session_id": "session456"
    },
    headers={"Authorization": f"Bearer {token}"}
)

print("对话回复:", dialogue_response.json())
```

### 2. 使用curl命令

```bash
# examples/api_curl.sh

# 健康检查
curl http://localhost:8000/health

# 登录
curl -X POST http://localhost:8000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# 发送消息
curl -X POST http://localhost:8000/api/v2/dialogue/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"message":"你好","user_id":"user123","session_id":"session456"}'
```

---

## 插件开发示例

### 1. 自定义插件

```python
# examples/custom_plugin.py
from src.wuqu.plugin_system import PluginSystem, BasePlugin

class CustomPlugin(BasePlugin):
    """自定义插件示例"""
    
    def __init__(self):
        super().__init__()
        self.name = "custom_plugin"
        self.version = "1.0.0"
    
    def execute(self, params):
        """执行插件逻辑"""
        # 自定义逻辑
        result = {
            "plugin": self.name,
            "version": self.version,
            "params": params,
            "result": "插件执行成功"
        }
        return result
    
    def validate(self, params):
        """验证参数"""
        return True

# 注册插件
plugin_system = PluginSystem()
plugin_system.register(CustomPlugin())

# 执行插件
result = plugin_system.execute("custom_plugin", {"action": "test"})
print("插件执行结果:", result)
```

---

## 集成示例

### 1. Flask集成

```python
# examples/flask_integration.py
from flask import Flask, request, jsonify
from src.ziwei.intent_recognition import IntentRecognition

app = Flask(__name__)
recognizer = IntentRecognition()

@app.route('/api/intent', methods=['POST'])
def recognize_intent():
    """意图识别API"""
    data = request.json
    text = data.get('text', '')
    
    result = recognizer.recognize(text)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 2. Django集成

```python
# examples/django_integration.py
from django.http import JsonResponse
from django.views import View
from src.ziwei.intent_recognition import IntentRecognition

class IntentRecognitionView(View):
    """意图识别视图"""
    
    def post(self, request):
        """POST请求处理"""
        import json
        data = json.loads(request.body)
        text = data.get('text', '')
        
        recognizer = IntentRecognition()
        result = recognizer.recognize(text)
        
        return JsonResponse(result)
```

### 3. FastAPI集成

```python
# examples/fastapi_integration.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.ziwei.intent_recognition import IntentRecognition

app = FastAPI()
recognizer = IntentRecognition()

class IntentRequest(BaseModel):
    text: str

@app.post("/api/intent")
async def recognize_intent(request: IntentRequest):
    """意图识别API"""
    result = recognizer.recognize(request.text)
    
    if result is None:
        raise HTTPException(status_code=400, detail="意图识别失败")
    
    return result
```

---

## 高级示例

### 1. 异步处理

```python
# examples/async_processing.py
import asyncio
from src.pohjun.task_execute_yun import TaskExecutor

async def process_tasks():
    """异步处理任务"""
    executor = TaskExecutor()
    
    tasks = [
        {"id": i, "task": f"任务{i}"}
        for i in range(10)
    ]
    
    results = await asyncio.gather(*[
        executor.execute_async(task)
        for task in tasks
    ])
    
    return results

# 运行异步处理
results = asyncio.run(process_tasks())
print("处理结果:", results)
```

### 2. 流式响应

```python
# examples/streaming_response.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def stream_response():
    """流式响应"""
    async def generate():
        for i in range(10):
            yield f"数据块 {i}\n"
            await asyncio.sleep(0.1)
    
    return StreamingResponse(generate())
```

---

## 更多示例

- 完整示例请查看 `examples/` 目录下的其他文件
- 更多文档请查看 `docs/` 目录
- API文档请查看 `docs/API.md`

---

**更新时间**: 2026-03-18
