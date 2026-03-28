# 小元（Xiaoyuan）API 接口文档

## 概述

小元是开发者端智能助手适配层，提供 API 管理、插件开发、SDK 管理和代码审查等核心能力。

## 基础信息

- **版本**: 1.0.0
- **基础 URL**: `http://localhost:5000/api/xiaoyuan`
- **认证方式**: Bearer Token
- **内容类型**: `application/json`

---

## 1. 会话管理

### 1.1 创建会话

创建新的开发者会话。

**请求**
```http
POST /api/xiaoyuan/sessions
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "userId": "developer_123",
  "metadata": {
    "platform": "web",
    "version": "1.0.0"
  }
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "id": "session_abc123",
    "userId": "developer_123",
    "messages": [],
    "context": {},
    "state": {
      "status": "connected",
      "lastActivity": 1711447200000
    },
    "createdAt": 1711447200000,
    "updatedAt": 1711447200000
  }
}
```

### 1.2 获取会话

获取指定会话信息。

**请求**
```http
GET /api/xiaoyuan/sessions/{session_id}
Authorization: Bearer {api_key}
```

### 1.3 删除会话

删除指定会话。

**请求**
```http
DELETE /api/xiaoyuan/sessions/{session_id}
Authorization: Bearer {api_key}
```

---

## 2. 消息处理

### 2.1 发送消息

发送消息给小元并获取响应。

**请求**
```http
POST /api/xiaoyuan/sessions/{session_id}/messages
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "type": "text",
  "content": "帮我生成一个 TypeScript 插件模板",
  "serviceType": "plugin_development",
  "metadata": {}
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "id": "msg_xyz789",
    "type": "text",
    "role": "assistant",
    "content": "我已经为您生成了插件模板...",
    "timestamp": 1711447260000,
    "serviceType": "plugin_development"
  }
}
```

### 2.2 获取消息历史

获取会话的消息历史。

**请求**
```http
GET /api/xiaoyuan/sessions/{session_id}/messages
Authorization: Bearer {api_key}
```

**响应**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "id": "msg_1",
        "type": "text",
        "role": "user",
        "content": "Hello",
        "timestamp": 1711447200000
      },
      {
        "id": "msg_2",
        "type": "text",
        "role": "assistant",
        "content": "Hi! How can I help you?",
        "timestamp": 1711447210000
      }
    ],
    "total": 2
  }
}
```

---

## 3. API 管理

### 3.1 获取所有 API 端点

获取已注册的所有 API 端点。

**请求**
```http
GET /api/xiaoyuan/api/endpoints
Authorization: Bearer {api_key}
```

**响应**
```json
{
  "success": true,
  "data": {
    "endpoints": [
      {
        "id": "api_1",
        "path": "/api/v1/users",
        "method": "GET",
        "description": "获取用户列表",
        "tags": ["users", "read"],
        "parameters": [],
        "responses": {
          "200": {
            "type": "array",
            "description": "用户列表"
          }
        },
        "authRequired": true
      }
    ],
    "total": 1
  }
}
```

### 3.2 获取单个 API 端点

根据 ID 获取 API 端点详情。

**请求**
```http
GET /api/xiaoyuan/api/endpoints/{endpoint_id}
Authorization: Bearer {api_key}
```

### 3.3 创建 API 端点

创建新的 API 端点。

**请求**
```http
POST /api/xiaoyuan/api/endpoints
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "path": "/api/v1/products",
  "method": "POST",
  "description": "创建产品",
  "tags": ["products", "write"],
  "parameters": [
    {
      "name": "name",
      "type": "string",
      "required": true,
      "description": "产品名称"
    },
    {
      "name": "price",
      "type": "number",
      "required": true,
      "description": "产品价格"
    }
  ],
  "authRequired": true
}
```

### 3.4 生成 API 文档

生成 API 文档（支持 Markdown、HTML、OpenAPI 格式）。

**请求**
```http
POST /api/xiaoyuan/api/documentation
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "format": "markdown"
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "format": "markdown",
    "content": "# API 文档\n\n## 概览\n...",
    "timestamp": 1711447300000
  }
}
```

### 3.5 测试 API

执行 API 测试请求。

**请求**
```http
POST /api/xiaoyuan/api/test
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "method": "GET",
  "url": "http://localhost:5000/api/v1/users",
  "headers": {
    "Authorization": "Bearer test_token"
  },
  "queryParams": {
    "page": "1",
    "limit": "10"
  }
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "status": 200,
    "headers": {},
    "body": {
      "users": []
    },
    "duration": 125,
    "timestamp": 1711447310000
  }
}
```

---

## 4. 插件开发

### 4.1 获取所有插件模板

获取可用的插件模板列表。

**请求**
```http
GET /api/xiaoyuan/plugins/templates
Authorization: Bearer {api_key}
```

**响应**
```json
{
  "success": true,
  "data": {
    "templates": [
      {
        "id": "typescript-basic-plugin",
        "name": "TypeScript 基础插件",
        "description": "一个简单的 TypeScript 插件模板",
        "category": "general",
        "type": "service",
        "language": "typescript",
        "dependencies": {}
      }
    ],
    "total": 1
  }
}
```

### 4.2 创建插件项目

基于模板创建插件项目。

**请求**
```http
POST /api/xiaoyuan/plugins/create
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "templateId": "typescript-basic-plugin",
  "pluginName": "My Plugin",
  "options": {
    "author": "Your Name",
    "email": "your.email@example.com"
  }
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "path": "src/index.ts",
        "content": "/**\n * 插件入口文件\n */...",
        "description": "插件主类"
      },
      {
        "path": "package.json",
        "content": "{\n  \"name\": \"my-plugin\"...",
        "description": "项目配置"
      }
    ],
    "totalFiles": 4
  }
}
```

### 4.3 生成插件 API 对接指南

生成插件 API 对接指南。

**请求**
```http
POST /api/xiaoyuan/plugins/guide
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "pluginId": "my-plugin",
  "apiEndpoints": [
    {
      "id": "ep1",
      "path": "/api/v1/data",
      "method": "GET",
      "description": "获取数据"
    }
  ]
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "pluginId": "my-plugin",
    "apiEndpoints": [...],
    "usageExamples": [...],
    "integrationSteps": [...],
    "testingGuide": {
      "unitTests": [...],
      "integrationTests": [...],
      "manualTests": [...]
    }
  }
}
```

---

## 5. SDK 管理

### 5.1 获取所有 SDK

获取所有可用的 SDK 信息。

**请求**
```http
GET /api/xiaoyuan/sdk/list
Authorization: Bearer {api_key}
```

**响应**
```json
{
  "success": true,
  "data": {
    "sdks": [
      {
        "name": "javascript",
        "currentVersion": "1.2.0",
        "latestVersion": "1.2.0",
        "platforms": ["Node.js", "Browser"],
        "languages": ["JavaScript", "TypeScript"],
        "documentationUrl": "https://docs.xuanji.ai/sdk/javascript"
      },
      {
        "name": "python",
        "currentVersion": "1.1.0",
        "latestVersion": "1.1.0",
        "platforms": ["Python 3.8+"],
        "languages": ["Python"],
        "documentationUrl": "https://docs.xuanji.ai/sdk/python"
      }
    ],
    "total": 2
  }
}
```

### 5.2 检查 SDK 更新

检查指定 SDK 是否有可用更新。

**请求**
```http
GET /api/xiaoyuan/sdk/{sdk_name}/updates
Authorization: Bearer {api_key}
```

**响应**
```json
{
  "success": true,
  "data": {
    "sdkName": "javascript",
    "fromVersion": "1.1.0",
    "toVersion": "1.2.0",
    "type": "minor",
    "changes": [
      "新增批量操作 API",
      "优化错误处理机制"
    ],
    "breakingChanges": [],
    "migrationGuide": [...]
  }
}
```

### 5.3 获取 SDK 集成指南

获取 SDK 集成指南。

**请求**
```http
GET /api/xiaoyuan/sdk/{sdk_name}/guide?platform=node.js&language=typescript
Authorization: Bearer {api_key}
```

**响应**
```json
{
  "success": true,
  "data": {
    "sdkName": "javascript",
    "platform": "node.js",
    "language": "typescript",
    "installationSteps": [
      "npm install @xuanji-ai/sdk"
    ],
    "configurationSteps": [...],
    "usageExamples": [...],
    "commonIssues": [...]
  }
}
```

### 5.4 获取 SDK 版本历史

获取 SDK 版本历史。

**请求**
```http
GET /api/xiaoyuan/sdk/{sdk_name}/versions
Authorization: Bearer {api_key}
```

---

## 6. 代码审查

### 6.1 审查代码

提交代码进行审查。

**请求**
```http
POST /api/xiaoyuan/review
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "code": "function example() {\n  console.log('Hello');\n}",
  "language": "javascript",
  "filePath": "src/example.js",
  "rules": [
    {
      "id": "no-console-log",
      "enabled": true
    }
  ]
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "overallScore": 85,
    "summary": "代码质量良好。发现 1 个低优先级问题。",
    "issues": [
      {
        "id": "issue_1",
        "category": "quality",
        "severity": "low",
        "title": "生产代码不应包含 console.log",
        "description": "生产代码中不应保留调试日志",
        "line": 2,
        "rule": "no-console-log",
        "codeSnippet": "  console.log('Hello');",
        "suggestedFix": "移除或替换为适当的日志系统"
      }
    ],
    "suggestions": [
      {
        "type": "modernize",
        "title": "使用现代变量声明",
        "description": "将 var 替换为 let 或 const",
        "impact": "low"
      }
    ],
    "metrics": {
      "linesOfCode": 3,
      "complexity": 1,
    },
    "timestamp": 1711447400000
  }
}
```

### 6.2 扫描安全漏洞

扫描代码中的安全漏洞。

**请求**
```http
POST /api/xiaoyuan/review/security
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "code": "const password = 'secret123';",
  "language": "javascript",
  "filePath": "src/config.js"
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "vulnerabilities": [
      {
        "id": "vuln_1",
        "severity": "high",
        "cwe": "CWE-798",
        "title": "硬编码凭据",
        "description": "代码中包含硬编码的密码或密钥",
        "location": {
          "file": "src/config.js",
          "line": 1,
          "column": 1
        },
        "codeSnippet": "const password = 'secret123';",
        "recommendation": "使用环境变量或密钥管理服务存储凭据",
        "references": [
          "https://cwe.mitre.org/data/definitions/798"
        ]
      }
    ],
    "total": 1
  }
}
```

### 6.3 获取审查规则

获取所有可用的代码审查规则。

**请求**
```http
GET /api/xiaoyuan/review/rules
Authorization: Bearer {api_key}
```

---

## 7. 系统管理

### 7.1 健康检查

检查适配器健康状态。

**请求**
```http
GET /api/xiaoyuan/health
```

**响应**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": 1711447500000,
    "services": {
      "apiManagement": "running",
      "pluginDevelopment": "running",
      "sdkManagement": "running",
      "codeReview": "running"
    },
    "connection": {
      "status": "connected",
      "uptime": 3600
    }
  }
}
```

### 7.2 获取配置

获取适配器配置信息。

**请求**
```http
GET /api/xiaoyuan/config
Authorization: Bearer {api_key}
```

### 7.3 更新配置

更新适配器配置。

**请求**
```http
PATCH /api/xiaoyuan/config
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "services": {
    "codeReview": {
      "strictMode": true
    }
  },
  "developer": {
    "preferredLanguage": "typescript"
  }
}
```

---

## WebSocket 连接

小元支持 WebSocket 实时通信。

### 连接 URL

```
ws://localhost:5000/ws/xiaoyuan?token={api_key}
```

### 消息格式

**客户端发送**
```json
{
  "type": "message",
  "sessionId": "session_abc123",
  "payload": {
    "type": "text",
    "content": "Hello",
    "serviceType": "api_management"
  }
}
```

**服务端响应**
```json
{
  "type": "response",
  "messageId": "msg_xyz789",
  "payload": {
    "type": "text",
    "content": "Hi! How can I help?",
    "role": "assistant",
    "timestamp": 1711447600000
  }
}
```

### 消息类型

| 类型 | 描述 |
|------|------|
| `connect` | 连接建立 |
| `message` | 客户端消息 |
| `response` | 服务端响应 |
| `heartbeat` | 心跳包 |
| `notification` | 系统通知 |
| `close` | 连接关闭 |
| `error` | 错误消息 |

---

## 错误码

| 错误码 | HTTP 状态码 | 描述 |
|--------|-------------|------|
| `INVALID_REQUEST` | 400 | 请求参数无效 |
| `UNAUTHORIZED` | 401 | 未授权或 API Key 无效 |
| `FORBIDDEN` | 403 | 权限不足 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `RATE_LIMITED` | 429 | 请求频率超限 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |
| `SERVICE_UNAVAILABLE` | 503 | 服务不可用 |

---

## 示例

### 示例 1: 完整的会话流程

```javascript
// 1. 创建会话
const sessionResponse = await fetch('/api/xiaoyuan/sessions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    userId: 'developer_123'
  })
});
const session = await sessionResponse.json();

// 2. 发送消息
const messageResponse = await fetch(`/api/xiaoyuan/sessions/${session.data.id}/messages`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    type: 'text',
    content: '帮我生成一个 API 文档',
    serviceType: 'api_management'
  })
});
const message = await messageResponse.json();

console.log(message.data.content);
```

### 示例 2: 代码审查流程

```javascript
// 提交代码进行审查
const reviewResponse = await fetch('/api/xiaoyuan/review', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    code: `
      function processData(data) {
        const result = [];
        for (let i = 0; i < data.length; i++) {
          for (let j = 0; j < data[i].items.length; j++) {
            result.push(data[i].items[j]);
          }
        }
        return result;
      }
    `,
    language: 'javascript'
  })
});

const review = await reviewResponse.json();
console.log('代码评分:', review.data.overallScore);
console.log('发现问题:', review.data.issues.length);
```

---

## 版本历史

- **1.0.0** (2026-03-26)
  - 初始版本发布
  - 支持 API 管理、插件开发、SDK 管理、代码审查
  - 提供 REST API 和 WebSocket 接口
