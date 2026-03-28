# 小紫 - 用户端智能助手适配层 API 文档

## 概述

小紫（Xiaopurple）是紫微元灵的用户端智能助手适配层，提供对话、智能引导、推荐、诊断和自动化等功能。

## 目录

- [基础架构](#基础架构)
- [对话接口](#对话接口)
- [智能引导](#智能引导)
- [推荐引擎](#推荐引擎)
- [问题诊断](#问题诊断)
- [自动化操作](#自动化操作)
- [事件系统](#事件系统)

---

## 基础架构

### 初始化适配器

```typescript
import { XiaopurpleAdapter, defaultConfig } from './src';

// 创建适配器实例
const adapter = new XiaopurpleAdapter(defaultConfig);

// 启动适配器
await adapter.start();
```

### 健康检查

```typescript
// 获取健康状态
const health = adapter.healthCheck();
console.log(health);
// {
//   healthy: true,
//   details: {
//     connectionState: 'connected',
//     wsConnected: true,
//     conversationId: 'xp_1234567890_abc123',
//     messageCount: 5,
//     uptime: 3600000
//   }
// }
```

---

## 对话接口

### 发送文本消息

```typescript
import { MessageType, MessageRole } from './src';

const message = {
  id: generateId(),
  type: MessageType.TEXT,
  role: MessageRole.USER,
  content: '你好，请帮我分析数据',
  timestamp: Date.now()
};

await adapter.sendMessage(message);
```

### 发送语音消息

```typescript
const voiceMessage = {
  id: generateId(),
  type: MessageType.VOICE,
  role: MessageRole.USER,
  audioData: base64AudioData,
  duration: 15000,  // 毫秒
  timestamp: Date.now()
};

await adapter.sendMessage(voiceMessage);
```

### 接收消息流

```typescript
// 监听消息接收事件
adapter.on('message:received', (event) => {
  const message = event.data.message;
  console.log('收到消息:', message);

  if (message.type === MessageType.TEXT) {
    console.log('文本内容:', message.content);
  } else if (message.type === MessageType.VOICE) {
    console.log('语音转录:', message.transcript);
  }
});
```

### 获取对话历史

```typescript
// 获取所有历史消息
const history = adapter.getConversationHistory();

// 清空历史
adapter.clearHistory();
```

---

## 智能引导

### 初始化引导引擎

```typescript
import { GuideEngine } from './src';

const guideEngine = new GuideEngine();
```

### 开始引导流程

```typescript
// 开始新用户引导
const guideState = await guideEngine.startGuide(
  'new_user_onboarding',
  userId
);

if (guideState) {
  console.log('引导已开始:', guideState.currentStepId);
}
```

### 获取当前步骤

```typescript
const currentStep = guideEngine.getCurrentStep(userId, 'new_user_onboarding');

if (currentStep) {
  console.log('当前步骤:', currentStep.title);
  console.log('内容:', currentStep.content);

  if (currentStep.actionable) {
    // 显示可执行的操作
    currentStep.actions?.forEach(action => {
      console.log('操作:', action.label);
    });
  }
}
```

### 完成当前步骤

```typescript
// 完成当前步骤，自动进入下一步
const nextStep = await guideEngine.completeStep(userId, 'new_user_onboarding');

if (nextStep) {
  console.log('下一步:', nextStep.title);
} else {
  console.log('引导流程已完成');
}
```

### 推荐引导

```typescript
// 根据上下文推荐引导
const context = {
  userId,
  action: 'configure',
  features: ['settings', 'customization']
};

const recommendations = guideEngine.recommendGuides(context);

recommendations.forEach(guide => {
  console.log('推荐引导:', guide.name);
  console.log('描述:', guide.description);
});
```

---

## 推荐引擎

### 初始化推荐引擎

```typescript
import { RecommendationEngine } from './src';

const recommendationEngine = new RecommendationEngine();
```

### 设置用户画像

```typescript
const userProfile = {
  userId: 'user123',
  preferences: { theme: 'dark', language: 'zh-CN' },
  behaviors: [],
  skillLevel: 'intermediate',
  lastActiveTime: Date.now()
};

recommendationEngine.setUserProfile(userProfile);
```

### 追踪用户行为

```typescript
await recommendationEngine.trackBehavior(
  'configure_settings',
  {
    success: true,
    duration: 5000
  },
  ['settings', 'theme']
);
```

### 获取推荐

```typescript
// 获取所有推荐
const recommendations = recommendationEngine.getRecommendations(5);

recommendations.forEach(rec => {
  console.log('推荐:', rec.title);
  console.log('类型:', rec.type);
  console.log('置信度:', rec.confidence);

  if (rec.actions) {
    rec.actions.forEach(action => {
      console.log('操作:', action.label);
    });
  }
});
```

### 应用/驳回推荐

```typescript
// 应用推荐
await recommendationEngine.applyRecommendation(
  recommendationId,
  actionPayload
);

// 驳回推荐
await recommendationEngine.dismissRecommendation(recommendationId);
```

---

## 问题诊断

### 初始化诊断引擎

```typescript
import { DiagnosticEngine } from './src';

const diagnosticEngine = new DiagnosticEngine();
```

### 执行诊断

```typescript
// 提供症状
const symptoms = [
  '连接失败',
  '无法访问服务器',
  '网络错误'
];

const result = await diagnosticEngine.diagnose(symptoms);

console.log('问题类型:', result.issueType);
console.log('严重程度:', result.severity);
console.log('描述:', result.description);

// 查看解决方案
result.solutions.forEach(solution => {
  console.log('方案:', solution.title);
  console.log('描述:', solution.description);
  console.log('步骤:', solution.steps);
  console.log('可自动修复:', solution.autoFix);
});
```

### 执行解决方案

```typescript
const executionResult = await diagnosticEngine.executeSolution(
  result.id,
  solutionId
);

if (executionResult.success) {
  console.log('修复成功:', executionResult.message);
} else {
  console.log('修复失败:', executionResult.message);
}
```

### 获取人工支持

```typescript
const supportInfo = diagnosticEngine.getHumanSupportInfo();

if (supportInfo.available) {
  console.log('人工支持可用');
  supportInfo.channels.forEach(channel => {
    console.log(`${channel.type}: ${channel.contact}`);
  });
  console.log(`预计等待时间: ${supportInfo.estimatedWaitTime} 秒`);
}
```

---

## 自动化操作

### 初始化自动化引擎

```typescript
import { AutomationEngine } from './src';

const automationEngine = new AutomationEngine(true);  // 需要确认
```

### 创建自动化任务

```typescript
// 创建导航任务
const navigationTask = automationEngine.createTask(
  'navigation',
  '自动导航',
  [
    {
      id: 'nav_1',
      type: 'navigation',
      value: 'https://example.com'
    },
    {
      id: 'wait_1',
      type: 'wait',
      value: 2000
    },
    {
      id: 'click_1',
      type: 'click',
      selector: '#submit-button'
    }
  ]
);

console.log('任务已创建:', navigationTask.id);
```

### 执行任务

```typescript
// 执行任务（需要确认）
const result = await automationEngine.executeTask(
  navigationTask.id,
  true  // 确认执行
);

console.log('任务状态:', result.status);
console.log('结果:', result.result);
```

### 批量操作

```typescript
// 批量导航
const batchNavTask = automationEngine.createBatchNavigationTask([
  'https://example.com/page1',
  'https://example.com/page2',
  'https://example.com/page3'
]);

// 批量表单填写
const batchFormTask = automationEngine.createBatchFormFillTask([
  {
    selector: '#form1',
    data: {
      username: 'user1',
      email: 'user1@example.com'
    }
  },
  {
    selector: '#form2',
    data: {
      username: 'user2',
      email: 'user2@example.com'
    }
  }
]);
```

### 任务管理

```typescript
// 获取任务状态
const status = automationEngine.getTaskStatus(taskId);

// 获取所有任务
const allTasks = automationEngine.getAllTasks();
console.log('待执行:', allTasks.pending.length);
console.log('运行中:', allTasks.running.length);
console.log('已完成:', allTasks.completed.length);

// 取消任务
automationEngine.cancelTask(taskId);
```

---

## 事件系统

### 监听事件

```typescript
// 适配器启动
adapter.on('adapter:started', (event) => {
  console.log('适配器已启动');
});

// 消息发送
adapter.on('message:sent', (event) => {
  console.log('消息已发送:', event.data.message);
});

// 消息接收
adapter.on('message:received', (event) => {
  console.log('收到消息:', event.data.message);
});

// WebSocket 连接事件
adapter.on('ws:connected', () => {
  console.log('WebSocket 已连接');
});

adapter.on('ws:disconnected', () => {
  console.log('WebSocket 已断开');
});

adapter.on('ws:error', (event) => {
  console.error('WebSocket 错误:', event.data.error);
});
```

### 取消监听

```typescript
function handleReceivedMessage(event) {
  console.log('收到消息:', event.data.message);
}

// 监听
adapter.on('message:received', handleReceivedMessage);

// 取消监听
adapter.off('message:received', handleReceivedMessage);
```

---

## 完整示例

```typescript
import {
  XiaopurpleAdapter,
  GuideEngine,
  RecommendationEngine,
  DiagnosticEngine,
  AutomationEngine,
  defaultConfig,
  MessageType,
  MessageRole
} from './src';

async function main() {
  // 1. 初始化适配器
  const adapter = new XiaopurpleAdapter(defaultConfig);
  await adapter.start();

  // 2. 初始化各引擎
  const guideEngine = new GuideEngine();
  const recommendationEngine = new RecommendationEngine();
  const diagnosticEngine = new DiagnosticEngine();
  const automationEngine = new AutomationEngine();

  // 3. 设置事件监听
  adapter.on('message:received', async (event) => {
    const message = event.data.message;

    if (message.type === MessageType.TEXT) {
      const content = message.content;

      // 追踪用户行为
      await recommendationEngine.trackBehavior('send_message', {
        contentLength: content.length
      });

      // 自动诊断问题
      if (content.includes('错误') || content.includes('失败')) {
        const result = await diagnosticEngine.diagnose([content]);
        if (result.solutions.length > 0) {
          // 提供解决方案
          const reply = {
            id: generateId(),
            type: MessageType.TEXT,
            role: MessageRole.ASSISTANT,
            content: `检测到问题:${result.title}\n解决方案: ${result.solutions[0].title}`,
            timestamp: Date.now()
          };
          await adapter.sendMessage(reply);
        }
      }
    }
  });

  // 4. 开始新用户引导（如果是新用户）
  const isNewUser = true;
  if (isNewUser) {
    await guideEngine.startGuide('new_user_onboarding', 'user123');
  }

  // 5. 获取推荐
  const recommendations = recommendationEngine.getRecommendations(3);
  console.log('推荐:', recommendations);

  console.log('小紫适配器已就绪！');
}

main().catch(console.error);
```

---

## 类型定义

所有 API 的类型定义都在 `types/index.ts` 中，主要类型包括：

- `Message` - 消息类型
- `Conversation` - 对话会话
- `GuideFlow` - 引导流程
- `GuideStep` - 引导步骤
- `Recommendation` - 推荐项
- `DiagnosticResult` - 诊断结果
- `AutomationTask` - 自动化任务

详细类型定义请参考源文件。

---

## 错误处理

所有异步操作都可能抛出错误，建议使用 try-catch 处理：

```typescript
try {
  await adapter.sendMessage(message);
} catch (error) {
  console.error('发送消息失败:', error);

  // 可以使用诊断引擎分析错误
  const result = await diagnosticEngine.diagnose([
    '消息发送失败',
    error.message
  ]);
}
```

---

## 配置选项

配置项说明：

- `coreApiUrl` - 核心 API 地址
- `wsEndpoint` - WebSocket 端点
- `dialog` - 对话配置（历史长度、超时、语音、流式）
- `guidance` - 引导配置（启用、自动开始、跳过阈值）
- `recommendation` - 推荐配置（启用、最大数量、行为保留天数）
- `diagnostic` - 诊断配置（启用、自动诊断、最大重试）
- `automation` - 自动化配置（启用、确认要求、最大并发任务）
- `logging` - 日志配置（级别、控制台输出）

---

## 性能建议

1. **消息缓存**: 使用 `maxHistoryLength` 限制历史消息数量
2. **行为清理**: 定期调用 `cleanExpiredBehaviors()` 清理过期行为
3. **任务管理**: 清理已完成的自动化任务以释放内存
4. **事件清理**: 不再需要的事件监听器应该取消监听

---

## 安全建议

1. **确认执行**: 自动化操作默认需要用户确认
2. **敏感数据**: 不要在消息中包含密钥或密码
3. **输入验证**: 验证所有用户输入
4. **错误处理**: 适当的错误处理避免信息泄露

---

## 版本信息

- **版本**: 1.0.0
- **更新日期**: 2026-03-26
- **维护者**: 紫微元灵团队
