# 玄玑AI数字员工引擎 - 用户指南

**版本**: v2.0
**更新时间**: 2026-03-18

---

## 📋 目录

- [快速开始](#快速开始)
- [核心功能](#核心功能)
- [使用场景](#使用场景)
- [最佳实践](#最佳实践)
- [进阶功能](#进阶功能)

---

## 快速开始

### 安装

```bash
# 克隆代码仓库
git clone https://github.com/xuanji-ai-2026/xuanji-engine.git
cd xuanji-engine

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入实际配置
```

### 运行

```bash
# 启动服务
python -m src.api.main

# 或使用uvicorn
uvicorn src.api.main:app --host 0.0.0.0 --port 8080
```

### 测试

```bash
# 测试健康检查
curl http://localhost:8080/health

# 测试API
curl http://localhost:8080/api/v2/dialogue/message \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"你好","user_id":"test_user","session_id":"test_session"}'
```

---

## 核心功能

### 1. 意图识别

自动识别用户输入的意图和实体。

**使用示例**：
```python
from src.ziwei.intent_recognition import IntentRecognition

recognizer = IntentRecognition()
result = recognizer.recognize("帮我查询一下明天的天气")

print(result)
# {'intent': 'weather_query', 'confidence': 0.95, 'entities': {...}}
```

**支持的意图类型**：
- 天气查询
- 时间查询
- 信息查询
- 任务执行
- 对话闲聊

### 2. 对话管理

管理对话状态和上下文。

**使用示例**：
```python
from src.tanlang.dialog_manage_lei import DialogueManager

manager = DialogueManager()
response = manager.generate_response(
    intent="weather_query",
    user_id="user123",
    context={"location": "北京"}
)

print(response)
# {'reply': '明天北京的天气是晴天，温度15-25度', ...}
```

### 3. 记忆存储

存储和检索用户记忆。

**使用示例**：
```python
from src.jumen.memory_storage_shen import MemoryStorage
from src.jumen.memory_retrieve_han import MemoryRetrieve

# 存储记忆
storage = MemoryStorage()
memory_id = storage.store(None, {
    "user_id": "user123",
    "content": "用户喜欢看科幻电影",
    "type": "preference"
})

# 检索记忆
retrieve = MemoryRetrieve()
memory = retrieve.retrieve(None, memory_id)
```

### 4. 个性化服务

提供个性化配置和服务。

**使用示例**：
```python
from src.lianzheng.personality import Personality

personality = Personality()
config = personality.get_config("user123")

print(config)
# {'tone': 'friendly', 'style': 'professional', ...}
```

---

## 使用场景

### 场景1：智能客服

玄玑AI数字员工可以：
- 自动识别客户问题
- 提供准确答案
- 记住客户偏好
- 持续优化服务

### 场景2：个人助手

作为个人助手，可以：
- 管理日程
- 提醒事项
- 信息查询
- 任务执行

### 场景3：企业服务

为企业提供：
- 内部知识库
- 自动化流程
- 数据分析
- 智能推荐

---

## 最佳实践

### 1. 使用对话上下文

```python
# 维护对话历史
context = {
    "user_id": "user123",
    "session_id": "session456",
    "conversation_history": []
}

# 每次对话都更新上下文
response = manager.generate_response(
    message="用户消息",
    context=context
)
context["conversation_history"].append(response)
```

### 2. 缓存常用查询

```python
from src.jumen.memory_index_yang import MemoryIndex

# 创建索引加速查询
index = MemoryIndex()
index.create(db_session, memory_id, content)
```

### 3. 错误处理

```python
try:
    result = recognizer.recognize(text)
except Exception as e:
    # 记录错误
    logger.error(f"Intent recognition failed: {e}")
    # 返回默认意图
    result = {"intent": "unknown", "confidence": 0.0}
```

### 4. 性能优化

- 使用缓存减少重复计算
- 使用异步操作提高并发
- 使用连接池优化数据库访问

---

## 进阶功能

### 1. 自定义意图

```python
# 定义自定义意图
custom_intents = {
    "custom_action": {
        "keywords": ["自定义", "动作"],
        "response": "这是自定义动作的响应"
    }
}

recognizer.add_intents(custom_intents)
```

### 2. 插件开发

```python
from src.wuqu.plugin_system import PluginSystem

# 开发自定义插件
class CustomPlugin:
    def __init__(self):
        self.name = "custom_plugin"

    def execute(self, params):
        # 插件逻辑
        return {"result": "插件执行结果"}

# 注册插件
plugin_system = PluginSystem()
plugin_system.register(CustomPlugin())
```

### 3. 批量处理

```python
from src.pohjun.task_execute_yun import TaskExecutor

executor = TaskExecutor()

# 批量执行任务
tasks = [
    {"id": i, "task": f"任务{i}"}
    for i in range(100)
]

results = executor.execute_batch(tasks)
```

### 4. 安全配置

```python
from src.youbi.security import Security

# 配置安全策略
security = Security()
security.configure({
    "auth_enabled": True,
    "rate_limit_enabled": True,
    "rate_limit_per_minute": 60
})
```

---

## 常见问题

### Q: 如何自定义对话回复？

A: 使用DialogueManager的自定义回复功能：
```python
manager = DialogueManager()
manager.add_custom_response("greeting", "您好！我是玄玑AI数字员工")
```

### Q: 如何提高识别准确率？

A: 提供更多训练数据，优化模型参数，使用上下文信息。

### Q: 如何处理大量并发请求？

A: 使用异步操作、连接池、负载均衡、HPA自动扩展。

### Q: 如何备份数据？

A: 使用数据库备份、Redis持久化、配置文件版本控制。

---

**文档版本**: v2.0
**更新时间**: 2026-03-18
