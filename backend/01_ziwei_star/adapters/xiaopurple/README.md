# 小紫（Xiaopurple）- 用户端智能助手适配层

## 📋 简介

小紫是紫微元灵的用户端智能助手适配层，负责将紫微元灵核心能力无缝集成到用户端应用中。它提供了完整的对话对话接口、智能引导、个性化推荐、问题（诊断）和自动化操作功能。

## ✨ 核心特性

### 1. 对话接口适配
- ✅ 支持文本、语音、图像等多种消息类型
- ✅ 实时消息流处理
- ✅ WebSocket 长连接管理
- ✅ 自动重连机制
- ✅ 消息历史管理

### 2. 智能引导引擎
- ✅ 新用户引导流程
- ✅ 功能发现引导
- ✅ 操作步骤提示
- ✅ 引导流程自定义
- ✅ 用户技能级别自适应

### 3. 智能推荐引擎
- ✅ 基于用户行为的个性化推荐
- ✅ 配置优化建议
- ✅ 功能点推荐
- ✅ 最佳实践提示
- ✅ 行为模式分析

### 4. 问题诊断模块
- ✅ 自动问题识别
- ✅ 多种解决方案提供
- ✅ 自动修复支持
- ✅ 人工支持入口
- ✅ 常见问题库

### 5. 自动化操作引擎
- ✅ 自动填写表单
- ✅ 自动导航
- ✅ 批量操作支持
- ✅ 任务队列管理
- ✅ 执行确认机制

## 📁 项目结构

```
xiaopurple/
├── types/
│   └── index.ts                 # 类型定义
├── src/
│   ├── XiaopurpleAdapter.ts     # 核心适配器
│   ├── GuideEngine.ts           # 智能引导引擎
│   ├── RecommendationEngine.ts  # 推荐引擎
│   ├── DiagnosticEngine.ts      # 问题诊断引擎
│   ├── AutomationEngine.ts      # 自动化操作引擎
│   └── index.ts                 # 主入口
├── config/
│   └── default.config.ts        # 默认配置
└── docs/
    ├── API.md                   # API 接口文档
    └── ReactIntegration.md      # React 集成示例
```

## 🚀 快速开始

### 1. 基础使用

```typescript
import { XiaopurpleAdapter, defaultConfig } from './src';

// 创建适配器
const adapter = new XiaopurpleAdapter(defaultConfig);

// 启动适配器
await adapter.start();

// 监听消息
adapter.on('message:received', (event) => {
  console.log('收到消息:', event.data.message);
});

// 健康检查
const health = adapter.healthCheck();
console.log(health);
```

### 2. 发送消息

```typescript
import { MessageType, MessageRole } from './src';

const message = {
  id: generateId(),
  type: MessageType.TEXT,
  role: MessageRole.USER,
  content: '你好，小紫',
  timestamp: Date.now()
};

await adapter.sendMessage(message);
```

### 3. 使用引导引擎

```typescript
import { GuideEngine } from './src';

const guideEngine = new GuideEngine();

// 开始新用户引导
const state = await guideEngine.startGuide('new_user_onboarding', userId);

// 获取当前步骤
const step = guideEngine.getCurrentStep(userId, 'new_user_onboarding');

// 完成当前步骤
const nextStep = await guideEngine.completeStep(userId, 'new_user_onboarding');
```

### 4. 使用推荐引擎

```typescript
import { RecommendationEngine } from './src';

const engine = new RecommendationEngine();

// 设置用户画像
engine.setUserProfile({
  userId: 'user123',
  preferences: {},
  behaviors: [],
  skillLevel: 'intermediate',
  lastActiveTime: Date.now()
});

// 追踪行为
await engine.trackBehavior('configure', {}, ['settings']);

// 获取推荐
const recommendations = engine.getRecommendations(5);
```

### 5. 使用诊断问题

```typescript
import { DiagnosticEngine } from './src';

const engine = new DiagnosticEngine();

// 诊断问题
const result = await engine.diagnose([
  '连接失败',
  '网络错误'
]);

// 查看解决方案
result.solutions.forEach(solution => {
  console.log('方案:', solution.title);
  console.log('步骤:', solution.steps);
});

// 执行解决方案
const executionResult = await engine.executeSolution(result.id, solutionId);
```

### 6. 使用自动化操作

```typescript
import { AutomationEngine } from './src';

const engine = new AutomationEngine(true);  // 需要确认

// 创建任务
const task = engine.createTask('navigation', '自动导航', [
  {
    id: 'nav_1',
    type: 'navigation',
    value: 'https://example.com'
  }
]);

// 执行任务
const result = await engine.executeTask(task.id, true);
```

## 🔧 配置选项

```typescript
const config: XiaopurpleConfig = {
  // 核心 API 地址
  coreApiUrl: 'http://localhost:8080/api',
  wsEndpoint: 'ws://localhost:8080/ws',

  // 对话配置
  dialog: {
    maxHistoryLength: 100,
    timeout: 30000,
    enableVoice: true,
    enableStream: true
  },

  // 引导配置
  guidance: {
    enabled: true,
    autoStartOnboarding: true,
    skipThreshold: 3
  },

  // 推荐配置
  recommendation: {
    enabled: true,
    maxRecommendations: 5,
    behaviorRetentionDays: 30,
    minConfidenceThreshold: 0.5
  },

  // 诊断配置
  diagnostic: {
    enabled: true,
    autoDiagnose: true,
    maxRetries: 3
  },

  // 自动化配置
  automation: {
    enabled: true,
    requireConfirmation: true,
    maxConcurrentTasks: 5
  },

  // 日志配置
  logging: {
    level: 'info',
    enableConsole: true
  }
};
```

## 📚 文档

- [API 接口文档](./docs/API.md) - 详细的 API 使用说明
- [React 集成示例](./docs/ReactIntegration.md) - React 前端集成完整示例

## 🔌 事件系统

适配器支持丰富的事件监听：

```typescript
// 适配器事件
adapter.on('adapter:started', handler);
adapter.on('adapter:stopped', handler);

// 消息事件
adapter.on('message:sent', handler);
adapter.on('message:received', handler);

// WebSocket 事件
adapter.on('ws:connected', handler);
adapter.on('ws:disconnected', handler);
adapter.on('ws:error', handler);

// 对话事件
adapter.on('conversation:state_updated', handler);
adapter.on('history:cleared', handler);
```

## 🛡️ 安全特性

1. **确认执行机制** - 自动化操作默认需要用户确认
2. **输入验证** - 所有用户输入都经过验证
3. **错误处理** - 完善的错误处理和恢复机制
4. **敏感数据保护** - 不在日志中记录敏感信息

## 📊 性能优化

1. **消息缓存限制** - 防止内存溢出
2. **行为记录清理** - 自动清理过期行为记录
3. **任务队列管理** - 限制并发任务数量
4. **事件监听器管理** - 支持取消监听避免内存泄漏

## 🎯 使用场景

1. **新用户引导** - 帮助新用户快速上手
2. **智能客服** - 提供智能问答和问题诊断
3. **个性化推荐** - 根据用户行为提供个性化建议
4. **自动化操作** - 减少重复性操作
5. **错误诊断** - 自动识别和解决常见问题

## 🔧 开发建议

1. 遵循 TypeScript 严格模式
2. 使用事件系统处理异步操作
3. 实现完善的错误处理
4. 添加适当的日志记录
5. 定期清理缓存和历史记录

## 📝 版本信息

- **版本**: 1.0.0
- **发布日期**: 2026-03-26
- **维护团队**: 紫微元灵团队

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**💜 小紫 - 让智能更贴近用户**
