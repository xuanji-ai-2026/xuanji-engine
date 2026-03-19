# 玄玑AI数字员工引擎 API 文档

**版本**: v2.0
**更新时间**: 2026-03-18

---

## 📋 目录

- [概述](#概述)
- [认证](#认证)
- [API端点](#api端点)
- [请求/响应格式](#请求响应格式)
- [错误码](#错误码)
- [示例](#示例)

---

## 概述

玄玑AI数字员工引擎提供RESTful API接口，支持意图识别、对话管理、记忆存储、个性化服务等核心功能。

**Base URL**: `https://xuanji-engine.xuanji-ai.com/api`

**API版本**: `v2.0`

---

## 认证

### Token认证

所有API请求都需要在Header中携带认证Token：

```
Authorization: Bearer <token>
```

### 获取Token

```
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400
  }
}
```

---

## API端点

### 意图识别 (Intent Recognition)

#### 识别用户意图

```
POST /api/v2/intent/recognize
```

**请求**:
```json
{
  "text": "帮我查询一下明天的天气",
  "context": {
    "user_id": "user123",
    "session_id": "session456"
  }
}
```

**响应**:
```json
{
  "code": 200,
  "message": "识别成功",
  "data": {
    "intent": "weather_query",
    "confidence": 0.95,
    "entities": {
      "time": "明天",
      "location": "当前位置"
    }
  }
}
```

### 对话管理 (Dialogue Management)

#### 发送消息

```
POST /api/v2/dialogue/message
```

**请求**:
```json
{
  "message": "你好",
  "user_id": "user123",
  "session_id": "session456"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "消息发送成功",
  "data": {
    "reply": "您好！我是玄玑AI数字员工，请问有什么可以帮助您的？",
    "dialogue_state": "greeting"
  }
}
```

### 记忆存储 (Memory)

#### 存储记忆

```
POST /api/v2/memory/store
```

**请求**:
```json
{
  "user_id": "user123",
  "content": "用户喜欢看科幻电影",
  "type": "preference",
  "timestamp": "2026-03-18T22:00:00Z"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "记忆存储成功",
  "data": {
    "memory_id": "mem_123456"
  }
}
```

### 个性化服务 (Personality)

#### 获取个性化配置

```
GET /api/v2/personality/{user_id}
```

**响应**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "user_id": "user123",
    "personality": {
      "tone": "friendly",
      "style": "professional",
      "preferences": {
        "language": "zh-CN",
        "timezone": "Asia/Shanghai"
      }
    }
  }
}
```

---

## 请求/响应格式

### 请求格式

所有POST请求使用`application/json`格式。

### 响应格式

所有响应统一使用以下格式：

```json
{
  "code": 200,
  "message": "成功",
  "data": {},
  "timestamp": "2026-03-18T22:00:00Z"
}
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

### 错误响应示例

```json
{
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "field": "text",
    "reason": "text字段不能为空"
  },
  "timestamp": "2026-03-18T22:00:00Z"
}
```

---

## 示例

### 完整对话流程

1. **登录获取Token**
```bash
curl -X POST https://xuanji-engine.xuanji-ai.com/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password"}'
```

2. **识别意图**
```bash
curl -X POST https://xuanji-engine.xuanji-ai.com/api/v2/intent/recognize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"text":"帮我查询一下明天的天气"}'
```

3. **发送消息**
```bash
curl -X POST https://xuanji-engine.xuanji-ai.com/api/v2/dialogue/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"message":"你好","user_id":"user123"}'
```

---

## 版本历史

- **v2.0** (2026-03-18): 初始版本，支持核心功能
