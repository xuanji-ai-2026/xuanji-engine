# 小灵（Xiaoling）- 管理端智能助手适配层

## 简介

小灵（Xiaoling）是紫微元灵核心能力的**管理端适配层**，专门为管理后台提供智能助手服务。通过WebSocket和HTTP API，为管理端提供系统总控、运营管理、UI配置、用户管理和数据统计等核心功能。

## 特性

- 🔌 **双通道通信**: 同时支持WebSocket和HTTP API
- 📊 **实时监控**: 系统状态、服务状态、性能指标实时推送
- 🎨 **UI配置**: 主题、布局的可视化配置和预览
- 📈 **数据分析**: 用户行为分析、活跃度统计、趋势预测
- 🔧 **服务管理**: 服务启停控制、批量用户操作
- 💾 **智能缓存**: 内置缓存机制，提升响应速度
- 🔄 **自动重连**: WebSocket断线自动重连
- 🎯 **类型安全**: 完整的TypeScript类型定义

## 目录结构

```
xiaoling/
├── config/
│   └── xiaoling.config.ts       # 配置文件
├── types/
│   └── xiaoling.types.ts        # 类型定义
├── src/
│   ├── XiaolingAdapter.ts       # 核心适配器类
│   ├── XiaolingService.ts       # 模拟服务端实现
│   └── index.ts                 # 入口文件
├── docs/
│   └── API.md                   # API接口文档
├── examples/
│   └── react-integration.tsx    # React集成示例
└── README.md                    # 本文件
```

## 快速开始

### 1. 安装

```bash
# 在项目中安装依赖（如果需要）
npm install @types/node
```

### 2. 基本使用

```typescript
import { XiaolingAdapter } from './src/XiaolingAdapter';

// 创建小灵实例
const xiaoling = new XiaolingAdapter({
  websocket: {
    enabled: true,
    url: 'ws://localhost:5000/xiaoling',
  },
  http: {
    baseUrl: 'http://localhost:5000/api/xiaoling',
  },
});

// 获取系统状态
async function checkSystemStatus() {
  const result = await xiaoling.getSystemStatus();

  if (result.success && result.data) {
    console.log('系统状态:', result.data.status);
    console.log('运行时间:', result.data.uptime);
  }
}

checkSystemStatus();
```

### 3. React集成

```tsx
import React, { useEffect, useState } from 'react';
import { XiaolingAdapter } from '../src/XiaolingAdapter';

const xiaoling = new XiaolingAdapter();

function SystemStatus() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    xiaoling.getSystemStatus().then(result => {
      if (result.success) {
        setStatus(result.data);
      }
    });
  }, []);

  return <div>系统状态: {status?.status}</div>;
}
```

详细React集成示例请参考: [examples/react-integration.tsx](./examples/react-integration.tsx)

## 核心功能

### 1. 系统总控

```typescript
// 获取系统状态
const status = await xiaoling.getSystemStatus();

// 获取所有服务状态
const services = await xiaoling.getServiceStatuses();

// 控制服务
await xiaoling.controlService({
  serviceName: 'api-gateway',
  action: 'restart',
});

// 获取性能指标
const metrics = await xiaoling.getPerformanceMetrics({
  start: Date.now() - 3600000,
  end: Date.now(),
});
```

### 2. 运营管理

```typescript
// 获取用户活跃度
const activities = await xiaoling.getUserActivities({
  start: Date.now() - 86400000,
  end: Date.now(),
});

// 获取活跃度分析
const analytics = await xiaoling.getActivityAnalytics('daily');

// 获取运营策略
const strategies = await xiaoling.getOperationStrategies();

// 生成报表
const report = await xiaoling.generateReport({
  type: 'user_activity',
  period: { start: ..., end: ... },
  metrics: ['active_users'],
  format: 'excel',
});
```

### 3. UI配置

```typescript
// 获取主题
const theme = await xiaoling.getTheme('light');

// 更新主题
await xiaoling.updateTheme('light', {
  colors: {
    primary: '#ff0000',
  },
});

// 获取布局
const layout = await xiaoling.getLayout('default');

// UI预览
const preview = await xiaoling.previewUI({
  theme: 'light',
  layout: 'default',
  screen: 'desktop',
});
```

### 4. 用户管理

```typescript
// 获取用户信息
const user = await xiaoling.getUserInfo('user-001');

// 搜索用户
const users = await xiaoling.searchUsers('zhangsan');

// 获取用户行为
const behavior = await xiaoling.getUserBehavior('user-001');

// 批量操作
const result = await xiaoling.batchUserOperation({
  operation: 'activate',
  userIds: ['user-001', 'user-002'],
});
```

### 5. 数据统计

```typescript
// 查询统计数据
const stats = await xiaoling.queryStatistics({
  metric: 'active_users',
  period: { start: ..., end: ... },
  granularity: 'day',
});

// 趋势分析
const trend = await xiaoling.getTrendAnalysis('active_users', {
  start: Date.now() - 604800000,
  end: Date.now(),
});

// 创建自定义报表
const report = await xiaoling.createCustomReport({
  name: '月度报表',
  query: { ... },
  visualization: { type: 'line' },
});
```

## WebSocket事件

监听实时数据推送：

```typescript
// 监听连接状态
xiaoling.on('connected', () => {
  console.log('已连接');
});

xiaoling.on('disconnected', () => {
  console.log('已断开');
});

// 监听系统指标更新
xiaoling.on('system:metrics', (data) => {
  console.log('性能指标:', data);
});

// 监听用户活跃度
xiaoling.on('users:activity', (data) => {
  console.log('活跃用户:', data.activeUsers);
});

// 移除监听
xiaoling.off('system:metrics', handler);
```

## 配置选项

```typescript
interface XiaolingConfig {
  // WebSocket 配置
  websocket: {
    enabled: boolean;          // 是否启用WebSocket
    url: string;               // WebSocket URL
    reconnectInterval: number;  // 重连间隔(ms)
    maxRetries: number;         // 最大重试次数
  };

  // HTTP API 配置
  http: {
    baseUrl: string;            // API基础URL
    timeout: number;            // 请求超时(ms)
    maxRetries: number;         // 最大重试次数
  };

  // 缓存配置
  cache: {
    enabled: boolean;           // 是否启用缓存
    ttl: number;                // 缓存有效期(秒)
    maxSize: number;            // 最大缓存数量
  };

  // 性能监控配置
  performance: {
    enabled: boolean;
    sampleRate: number;         // 采样率 0-1
    alertThreshold: {           // 告警阈值
      cpu: number;
      memory: number;
      responseTime: number;
    };
  };

  // 日志配置
  logging: {
    level: 'debug' | 'info' | 'warn' | 'error';
    enableConsole: boolean;
    enableFile: boolean;
    maxFileSize: number;
  };
}
```

## API文档

完整的API接口文档请参考: [docs/API.md](./docs/API.md)

## 错误处理

所有API调用都返回统一的响应格式：

```typescript
interface Response<T> {
  success: boolean;           // 是否成功
  data?: T;                   // 响应数据
  error?: {                   // 错误信息
    code: string;
    message: string;
    details?: any;
  };
  timestamp: number;          // 时间戳
}
```

使用示例：

```typescript
const result = await xiaoling.getSystemStatus();

if (result.success) {
  console.log('成功:', result.data);
} else {
  console.error('失败:', result.error?.message);
}
```

## 测试

使用模拟服务进行测试：

```typescript
import { XiaolingService } from './src/XiaolingService';

const service = new XiaolingService();

// 测试获取系统服务状态
const status = await service.getSystemStatus();
console.log(status);

// 测试获取性能指标
const metrics = await service.getPerformanceMetrics();
console.log(metrics);
```

## 清理资源

```typescript
// 在组件卸载或应用关闭时清理
xiaoling.destroy();
```

## 开发计划

- [ ] 添加更多的单元测试
- [ ] 添加Mock服务器的完整实现
- [ ] 支持更多的UI预览功能
- [ ] 添加请求取消支持
- [ ] 实现请求队列管理
- [ ] 添加更详细的性能分析工具

## 技术栈

- **语言**: TypeScript
- **通信**: WebSocket + HTTP
- **前端兼容**: React 18.3.1+
- **构建工具**: (可配置)

## 许可证

内部项目，版权所有

## 联系方式

- 项目负责人: 周董
- 项目名称: 玄玑引擎第三期
- 模块: 小灵（Xiaoling）管理端适配层

---

**小灵（Xiaoling）** - 让管理更智能 🚀
