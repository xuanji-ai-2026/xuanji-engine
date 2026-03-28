# 小微适配层

> 配置端智能助手适配层 - 让紫微元灵核心能力为配置端提供服务

**版本**: v1.0.0  
**开发者**: 玄玑引擎团队  
**许可证**: MIT

---

## 📋 目录

- [简介](#简介)
- [功能特性](#功能特性)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [API 文档](#api-文档)
- [集成示例](#集成示例)
- [配置说明](#配置说明)
- [开发指南](#开发指南)

---

## 简介

小微（Xiaowei）是玄玑引擎中专门为配置端设计的智能助手适配层。它作为紫微元灵核心（Ziwei Core）与配置端应用之间的桥梁，提供统一的接口来访问紫微元灵的各种核心能力。

### 核心价值

- **统一接口**: 为配置端提供统一、类型安全的 API 接口
- **智能辅助**: 工作台引导、快速建议、批量操作
- **安全可靠**: 完善的认证授权机制和配置验证
- **易于集成**: 简洁的 API 设计，支持 React/Vue 等主流框架

---

## 功能特性

### 1. 配置协助接口适配

- ✅ 配置项查询（支持通配符、分组）
- ✅ 配置项修改（支持验证和持久化）
- ✅ 配置验证（类型检查、规则验证）
- ✅ 批量配置操作（set、delete、reset）

### 2. 工作台协助实现

- ✅ 工作台流程引导
- ✅ 快速操作建议
- ✅ 批量配置管理
- ✅ 配置导入/导出（JSON、YAML、ENV）

### 3. 认证协助模块

- ✅ 用户认证协助（Token、Session、Certificate）
- ✅ 权限配置建议
- ✅ 安全设置检查
- ✅ 会话管理

### 4. 用户管理协助

- ✅ 用户信息查询（支持搜索、筛选）
- ✅ 用户配置建议
- ✅ 批量用户操作
- ✅ 用户统计信息

---

## 项目结构

```
xiaowei/
├── src/                    # 源代码目录
│   ├── index.ts           # 统一入口，导出所有类
│   ├── ConfigAdapter.ts   # 配置接口适配器
│   ├── WorkbenchHelper.ts  # 工作台助手
│   ├── AuthHelper.ts      # 认证助手
│   └── UserHelper.ts      # 用户管理助手
│
├── types/                  # TypeScript 类型定义
│   └── index.ts           # 所有接口和类型定义
│
├── config/                 # 配置文件
│   └── adapter.config.json # 适配器配置
│
├── docs/                   # 文档目录
│   └── API.md             # API 接口文档
│
├── examples/               # 示例代码
│   └── ReactIntegration.tsx # React 集成示例
│
├── package.json           # npm 包配置
└── README.md              # 本文件
```

---

## 快速开始

### 安装

```bash
npm install xuanji-xiaowei-adapter
```

### 基本使用

```typescript
import { createXiaoweiAdapter } from 'xuanji-xiaowei-adapter';

// 创建适配器实例
const adapter = createXiaoweiAdapter({
  coreWsUrl: 'ws://localhost:8001/ws',
  coreHttpUrl: 'http://localhost:8001',
  adapterId: 'my-app',
  authToken: 'your-auth-token'
});

// 连接到紫微元灵核心
await adapter.connect({
  onConnect: () => console.log('已连接'),
  onError: (err) => console.error('错误:', err)
});

// 查询配置
const configResponse = await adapter.config.queryConfig({
  keys: ['app.*']
});

console.log('配置:', configResponse.data);
```

---

## API 文档

完整的 API 文档请查看 [`docs/API.md`](docs/API.md)。

### 主要模块

| 模块 | 类名 | 描述 |
|------|------|------|
| 配置管理 | `ConfigAdapter` | 配置查询、修改、验证 |
| 工作台 | `WorkbenchHelper` | 工作台引导、建议、批量操作 |
| 认证 | `AuthHelper` | 用户认证、权限管理、安全检查 |
| 用户管理 | `UserHelper` | 用户查询、配置、批量操作 |

---

## 集成示例

### React 集成

完整的 React 集成示例请查看 [`examples/ReactIntegration.tsx`](examples/ReactIntegration.tsx)。

```typescript
import { createXiaoweiAdapter } from 'xuanji-xiaowei-adapter';
import { useState, useEffect } from 'react';

function ConfigComponent() {
  const [adapter] = useState(() => createXiaoweiAdapter({
    coreWsUrl: 'ws://localhost:8001/ws'
  }));

  useEffect(() => {
    adapter.connect();
    return () => adapter.disconnect();
  }, [adapter]);

  return (
    <div>
      {/* 你的组件内容 */}
    </div>
  );
}
```

---

## 配置说明

配置文件位于 `config/adapter.config.json`：

```json
{
  "adapter": {
    "name": "xiaowei",
    "version": "1.0.0",
    "description": "配置端面智能助手适配层 - 小微"
  },
  "core": {
    "wsUrl": "ws://localhost:8001/ws",
    "httpUrl": "http://localhost:8001"
  },
  "defaults": {
    "timeout": 30000,
    "logLevel": "info",
    "maxReconnectAttempts": 5,
    "reconnectDelay": 1000
  },
  "features": {
    "configManagement": true,
    "workbenchGuide": true,
    "authHelper": true,
    "userManager": true,
    "batchOperations": true
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `core.wsUrl` | string | - | 紫微元灵核心 WebSocket 地址 |
| `core.httpUrl` | string | - | 紫微元灵核心 HTTP 地址 |
| `timeout` | number | 30000 | 消息超时时间（毫秒） |
| `logLevel` | string | 'info' | 日志级别 |
| `maxReconnectAttempts` | number | 5 | 最大重连次数 |
| `reconnectDelay` | number | 1000 | 重连延迟（毫秒） |

---

## 开发指南

### 环境要求

- Node.js >= 16.0.0
- TypeScript >= 4.5.0

### 开发步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/xuanji-ai-2026/xuanji-engine.git
   cd xuanji-engine/backend/01_ziwei_star/adapters/xiaowei
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **构建项目**
   ```bash
   npm run build
   ```

4. **运行测试**
   ```bash
   npm test
   ```

5. **生成文档**
   ```bash
   npm run docs
   ```

### 代码规范

项目使用 ESLint 和 Prettier 进行代码规范检查：

```bash
# 检查代码规范
npm run lint

# 自动修复
npm run lint:fix
```

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 技术架构

### 架构图

```
┌─────────────────────────────────────────────────┐
│                 配置端应用                      │
│              (React/Vue/Angular)                │
└───────────────────┬─────────────────────────────┘
                    │
                    │ HTTP/WebSocket
                    │
┌───────────────────▼─────────────────────────────┐
│               小微适配层                        │
│  ┌──────────┬──────────┬──────────┬──────────┐│
│  │  配置    │  工作台  │  认证    │  用户    ││
│  │  适配器  │  助手    │  助手    │  助手    ││
│  └──────────┴──────────┴──────────┴──────────┘│
└───────────────────┬─────────────────────────────┘
                    │
                    │ WebSocket Message
                    │
┌───────────────────▼─────────────────────────────┐
│              紫微元灵核心                        │
│           (Ziwei Star Core)                      │
│                                                  │
│  ┌──────────────┬────────────────────────────┐ │
│  │  意图理解    │  智能推理                 │ │
│  └──────────────┴────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### 消息流程

1. **配置端应用** 调用小微适配层 API
2. **小微适配层** 封装消息，发送到紫微元灵核心
3. **紫微元灵核心** 处理消息，返回结果
4. **小微适配层** 解析响应，返回给配置端应用

---

## 常见问题

### Q: 如何处理连接断开？

A: 小微适配层内置了自动重连机制，默认会尝试重连 5 次。你可以通过配置调整重连参数：

```typescript
const adapter = createXiaoweiAdapter({
  coreWsUrl: 'ws://localhost:8001/ws',
  timeout: 60000,  // 增加超时时间
});

adapter.connect({
  onDisconnect: () => {
    console.log('连接断开，正在重连...');
  }
});
```

### Q: 如何调试消息？

A: 设置日志级别为 'debug'：

```typescript
const adapter = createXiaoweiAdapter({
  coreWsUrl: 'ws://localhost:8001/ws',
  logLevel: 'debug'  // 启用调试日志
});
```

### Q: 如何批量操作配置？

A: 使用 `batchConfig` 方法：

```typescript
const response = await adapter.config.batchConfig([
  { type: 'set', key: 'app.debug', value: false },
  { type: 'set', key: 'app.cache.enabled', value: true },
  { type: 'delete', key: 'app.legacy' }
]);
```

---

## 更新日志

### v1.0.0 (2026-03-26)

- ✨ 初始版本发布
- ✅ 实现配置协助接口适配
- ✅ 实现工作台协助
- ✅ 实现认证协助模块
- ✅ 实现用户管理协助
- ✅ 完整的 TypeScript 类型定义
- ✅ React 集成示例

---

## 许可证

MIT License - 详见 LICENSE 文件

---

## 联系方式

- 项目主页: https://github.com/xuanji-ai-2026/xuanji-engine
- 问题反馈: https://github.com/xuanji-ai-2026/xuanji-engine/issues
- 邮箱: support@xuanji.ai

---

**玄玑引擎团队** © 2026
