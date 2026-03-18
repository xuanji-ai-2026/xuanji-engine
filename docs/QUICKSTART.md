# 玄玑AI数字员工引擎 - 快速开始

**版本**: v2.0
**更新时间**: 2026-03-18

---

## 🚀 5分钟快速开始

### 第1步：安装（30秒）

```bash
# 克隆代码
git clone https://github.com/xuanji-ai-2026/xuanji-engine.git
cd xuanji-engine

# 安装依赖
pip install -r requirements.txt
```

### 第2步：配置（1分钟）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件
nano .env
```

**必需配置**：
```bash
# DeepSeek API
DEEPSEEK_API_KEY=your_api_key_here

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=xuanji_engine
DB_USER=xuanji
DB_PASSWORD=your_password_here

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password_here
```

### 第3步：启动（1分钟）

```bash
# 启动服务
python -m src.api.main

# 或使用uvicorn
uvicorn src.api.main:app --host 0.0.0.0 --port 8080
```

服务启动后，访问：http://localhost:8080

### 第4步：测试（1分钟）

```bash
# 测试健康检查
curl http://localhost:8080/health

# 测试对话API
curl -X POST http://localhost:8000/api/v2/dialogue/message \
  -H "Content-Type: application/json" \
  -d '{"message":"你好","user_id":"test_user","session_id":"test_session"}'
```

### 第5步：使用（剩余时间）

```python
# Python客户端示例
import httpx

# 创建客户端
client = httpx.AsyncClient(base_url="http://localhost:8000")

# 发送对话
response = await client.post(
    "/api/v2/dialogue/message",
    json={
        "message": "你好，我是新用户",
        "user_id": "new_user_123",
        "session_id": "new_session_456"
    }
)

# 打印回复
print(response.json()["data"]["reply"])
# 输出: 您好！我是玄玑AI数字员工，请问有什么可以帮助您的？
```

---

## 📚 更多资源

- **用户指南**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **API文档**: [docs/API.md](docs/API.md)
- **常见问题**: [docs/FAQ.md](docs/FAQ.md)
- **架构文档**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **部署文档**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **示例代码**: [examples/README.md](examples/README.md)

---

## 🎯 第一个程序

### Hello World示例

```python
# examples/hello_world.py
from src.tanlang.dialog_manage_lei import DialogueManager

# 初始化对话管理器
manager = DialogueManager()

# 生成问候回复
response = manager.generate_response(
    intent="greeting",
    user_id="hello_user"
)

print("玄玑AI:", response["reply"])
# 输出: 玄玑AI: 您好！我是玄玑AI数字员工，请问有什么可以帮助您的？
```

### 运行第一个程序

```bash
python examples/hello_world.py
```

---

## 🔧 故障排查

### 问题1：启动失败

**错误**: `ModuleNotFoundError: No module named 'src'`

**解决方案**：
```bash
# 添加当前目录到Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 或在启动脚本中设置
```

### 问题2：数据库连接失败

**错误**: `could not connect to server`

**解决方案**：
1. 检查PostgreSQL服务是否启动
2. 检查`.env`中的数据库配置
3. 检查防火墙设置

### 问题3：API调用失败

**错误**: `401 Unauthorized`

**解决方案**：
```bash
# 首先登录获取Token
curl -X POST http://localhost:8000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

---

## 📞 获取帮助

如果遇到问题：

1. 查看 [FAQ文档](docs/FAQ.md)
2. 查看 [部署文档](docs/DEPLOYMENT.md)
3. 提交 [GitHub Issue](https://github.com/xuanji-ai-2026/xuanji-engine/issues)

---

**快速开始完成！** 🎉

**更新时间**: 2026-03-18
