# 小微适配层 API 接口文档

**版本**: v1.0.0  
**描述**: 配置端智能助手适配层 API 文档

---

## 目录

- [快速开始](#快速开始)
- [配置接口](#配置接口)
- [工作台接口](#工作台接口)
- [认证接口](#认证接口)
- [用户管理接口](#用户管理接口)
- [WebSocket 消息格式](#websocket-消息格式)
- [错误处理](#错误处理)

---

## 快速开始

### 安装

```bash
npm install --save xuanji-xiaowei-adapter
```

### 初始化

```typescript
import { createXiaoweiAdapter } from 'xuanji-xiaowei-adapter';

// 创建适配器实例
const adapter = createXiaoweiAdapter({
  coreWsUrl: 'ws://localhost:8001/ws',
  coreHttpUrl: 'http://localhost:8001',
  adapterId: 'my-app-adapter',
  authToken: 'your-auth-token',
  logLevel: 'debug',
  timeout: 30000
});

// 连接到紫微元灵核心
await adapter.connect({
  onConnect: (data) => console.log('Connected!', data),
  onDisconnect: (data) => console.log('Disconnected', data),
  onMessage: (message) => console.log('Message:', message),
  onError: (error) => console.error('Error:', error)
});
```

---

## 配置接口

### 1. 查询配置项

**方法**: `adapter.config.queryConfig(params)`

**参数**:
```typescript
interface ConfigQueryParams {
  keys?: string[];           // 查询的配置键（支持通配符）
  group?: string;            // 分组
  includeDefault?: boolean;  // 是否返回默认值
}
```

**返回**:
```typescript
interface BaseResponse<ConfigItem[]> {
  status: 'success' | 'error' | 'partial';
  data?: ConfigItem[];
  error?: string;
  timestamp: number;
}
```

**示例**:
```typescript
const response = await adapter.config.queryConfig({
  keys: ['app.*', 'server.*'],
  includeDefault: true
});

if (response.status === 'success') {
  console.log('配置项:', response.data);
}
```

---

### 2. 修改配置项

**方法**: `adapter.config.modifyConfig(params)`

**参数**:
```typescript
interface ConfigModifyParams {
  items: Record<string, any>;  // 配置键值对
  validate?: boolean;          // 是否验证
  persist?: boolean;           // 是否持久化
}
```

**返回**:
```typescript
interface BaseResponse<{ success: boolean; updated: string[] }>
```

**示例**:
```typescript
const response = await adapter.config.modifyConfig({
  items: {
    'app.debug': false,
    'server.port': 3000
  },
  validate: true,
  persist: true
});
```

---

### 3. 验证配置

**方法**: `adapter.config.validateConfig(configs)`

**参数**: `Record<string, any>` - 配置键值对

**返回**:
```typescript
interface BaseResponse<ValidationResult> {
  status: string;
  data?: ValidationResult;
  error?: string;
  timestamp: number;
}

interface ValidationResult {
  valid: boolean;
  errors: ConfigValidationError[];
  warnings: string[];
}
```

**示例**:
```typescript
const response = await adapter.config.validateConfig({
  'server.port': 3000,
  'app.timeout': 5000
});

if (response.data?.valid) {
  console.log('配置验证通过');
} else {
  console.error('验证错误:', response.data?.errors);
}
```

---

### 4. 批量配置操作

**方法**: `adapter.config.batchConfig(operations)`

**参数**:
```typescript
interface BatchConfigOperation {
  type: 'set' | 'delete' | 'reset';
  key: string;
  value?: any;
}
```

**示例**:
```typescript
const response = await adapter.config.batchConfig([
  { type: 'set', key: 'app.debug', value: false },
  { type: 'set', key: 'app.cache.enabled', value: true },
  { type: 'delete', key: 'app.legacy.enabled' }
]);
```

---

## 工作台接口

### 1. 获取工作台引导流程

**方法**: `adapter.workbench.getGuide(taskType)`

**参数**: `taskType: string` - 任务类型（setup, configure, deploy, etc.）

**返回**:
```typescript
interface BaseResponse<WorkbenchGuide> {
  data?: {
    id: string;
    title: string;
    description: string;
    steps: WorkbenchStep[];
    estimatedTime: string;
  };
}
```

**示例**:
```typescript
const response = await adapter.workbench.getGuide('setup');
console.log('引导步骤:', response.data?.steps);
```

---

### 2. 获取快速操作建议

**方法**: `adapter.workbench.getSuggestions(context)`

**参数**:
```typescript
{
  currentPage?: string;
  userRole?: string;
  recentActions?: string[];
  configChanges?: string[];
}
```

**示例**:
```typescript
const response = await adapter.workbench.getSuggestions({
  currentPage: '/config/server',
  userRole: 'admin',
  recentActions: ['config.update']
});

response.data?.forEach(suggestion => {
  console.log(`建议: ${suggestion.title}`);
  console.log(`操作: ${suggestion.action} -> ${suggestion.target}`);
});
```

---

### 3. 导出配置

**方法**: `adapter.workbench.exportConfigs(format, filters)`

**参数**:
- `format`: 'json' | 'yaml' | 'env'
- `filters`: 过滤条件（可选）

**示例**:
```typescript
const response = await adapter.workbench.exportConfigs('yaml');
// 下载文件
downloadFile(response.data?.data, response.data?.filename);
```

---

### 4. 导入配置

**方法**: `adapter.workbench.importConfigs(data, format, validate)`

**示例**:
```typescript
const configData = `app:
  debug: false
  port: 3000`;

const response = await adapter.workbench.importConfigs(configData, 'yaml', true);
console.log(`导入成功: ${response.data?.imported} 项`);
```

---

## 认证接口

### 1. 验证用户认证

**方法**: `adapter.auth.verifyAuth(params)`

**参数**:
```typescript
interface AuthVerifyParams {
  userId: string;
  token?: string;
  type: 'token' | 'session' | 'certificate';
}
```

**返回**:
```typescript
interface BaseResponse<AuthResult> {
  data?: {
    success: boolean;
    user?: UserInfo;
    permissions?: string[];
    expiresAt?: number;
  };
}
```

**示例**:
```typescript
const response = await adapter.auth.verifyAuth({
  userId: 'user123',
  token: 'token123',
  type: 'token'
});

if (response.data?.success) {
  console.log('用户:', response.data.user);
  console.log('权限:', response.data.permissions);
}
```

---

### 2. 执行安全检查

**方法**: `adapter.auth.performSecurityCheck()`

**返回**:
```typescript
interface BaseResponse<SecurityCheckResult> {
  data?: {
    score: number;
    riskLevel: 'low' | 'medium' | 'high';
    issues: SecurityIssue[];
    recommendations: string[];
  };
}
```

**示例**:
```typescript
const response = await adapter.auth.performSecurityCheck();
console.log(`安全评分: ${response.data?.score}/100`);
console.log(`风险级别: ${response.data?.riskLevel}`);

response.data?.issues.forEach(issue => {
  console.log(`问题: ${issue.description} (${issue.severity})`);
});
```

---

### 3. 获取权限建议

**方法**: `adapter.auth.getPermissionSuggestions(role, context)`

**示例**:
```typescript
const response = await adapter.auth.getPermissionSuggestions('admin', {
  department: 'IT',
  responsibilities: ['config_management', 'user_admin']
});

console.log('推荐权限:', response.data?.recommended);
console.log('可选权限:', response.data?.optional);
```

---

### 4. 检查用户权限

**方法**: `adapter.auth.checkPermission(userId, permission)`

**示例**:
```typescript
const response = await adapter.auth.checkPermission('user123', 'config.update');
if (response.data?.granted) {
  console.log('用户有权限');
} else {
  console.log('权限不足:', response.data?.reason);
}
```

---

## 用户管理接口

### 1. 查询用户

**方法**: `adapter.user.queryUsers(params)`

**参数**:
```typescript
interface UserQueryParams {
  filters: UserFilter;
  pagination?: Pagination;
  sort?: Sort;
}
```

**示例**:
```typescript
const response = await adapter.user.queryUsers({
  filters: {
    status: 'active',
    role: 'admin'
  },
  pagination: {
    page: 1,
    pageSize: 20
  },
  sort: {
    field: 'username',
    direction: 'asc'
  }
});

console.log(`共 ${response.data?.total} 个用户`);
response.data?.users.forEach(user => {
  console.log(`- ${user.username} (${user.role})`);
});
```

---

### 2. 创建用户

**方法**: `adapter.user.createUser(userData)`

**参数**:
```typescript
{
  id?: string;
  username: string;
  role: string;
  department?: string;
  email?: string;
  password?: string;
}
```

**示例**:
```typescript
const response = await adapter.user.createUser({
  username: 'newuser',
  role: 'editor',
  department: 'Marketing',
  email: 'newuser@example.com',
  password: 'SecurePass123!'
});

if (response.status === 'success') {
  console.log('用户创建成功:', response.data);
}
```

---

### 3. 更新用户

**方法**: `adapter.user.updateUser(userId, updates)`

**示例**:
```typescript
const response = await adapter.user.updateUser('user123', {
  role: 'admin',
  department: 'IT'
});
```

---

### 4. 批量用户操作

**方法**: `adapter.user.batchUserOperations(operations)`

**参数**:
```typescript
interface BatchUserOperation {
  type: 'create' | 'update' | 'delete' | 'activate' | 'deactivate';
  userId?: string;
  userData?: Partial<UserInfo>;
  filter?: UserFilter;
}
```

**示例**:
```typescript
const response = await adapter.user.batchUserOperations([
  {
    type: 'activate',
    filter: { status: 'inactive', department: 'IT' }
  },
  {
    type: 'update',
    userId: 'user456',
    userData: { role: 'senior_editor' }
  }
]);

console.log(`成功: ${response.data?.successful}, 失败: ${response.data?.failed}`);
```

---

### 5. 获取用户统计

**方法**: `adapter.user.getUserStatistics()`

**示例**:
```typescript
const stats = await adapter.user.getUserStatistics();
console.log(`总用户: ${stats.data?.total}`);
console.log(`活跃用户: ${stats.data?.active}`);
console.log(`按角色分布:`, stats.data?.byRole);
```

---

## WebSocket 消息格式

### 消息结构

```typescript
interface Message {
  id: string;           // 消息 ID
  type: MessageType;    // 消息类型
  payload: any;         // 消息负载
  timestamp: number;    // 时间戳
}
```

### 消息类型枚举

```typescript
enum MessageType {
  // 配置相关
  CONFIG_QUERY = 'config.query',
  CONFIG_MODIFY = 'config.modify',
  CONFIG_VALIDATE = 'config.validate',
  CONFIG_BATCH = 'config.batch',
  
  // 工作台相关
  WORKBENCH_GUIDE = 'workbench.guide',
  WORKBENCH_SUGGEST = 'workbench.suggest',
  WORKBENCH_FLOW = 'workbench.flow',
  
  // 认证相关
  AUTH_VERIFY = 'auth.verify',
  AUTH_CONFIGURE = 'auth.configure',
  AUTH_SECURITY_CHECK = 'auth.security_check',
  
  // 用户管理相关
  USER_QUERY = 'user.query',
  USER_CONFIGURE = 'user.configure',
  USER_BATCH = 'user.batch',
  
  // 通用
  PING = 'ping',
  PONG = 'pong'
}
```

---

## 错误处理

所有 API 调用都返回 `BaseResponse<T>`，其中：

- `status`: 响应状态
  - `success`: 操作成功
  - `error`: 操作失败
  - `partial`: 部分成功（批量操作时）

- `error`: 错误消息（失败时存在）

### 错误处理示例

```typescript
try {
  const response = await adapter.config.modifyConfig({
    items: { 'server.port': 3000 }
  });

  if (response.status === 'success') {
    console.log('操作成功');
  } else {
    console.error('操作失败:', response.error);
  }
} catch (error) {
  console.error('网络错误或超时:', error);
}
```

---

## 完整示例

```typescript
import { createXiaoweiAdapter } from 'xuanji-xiaowei-adapter';

async function main() {
  // 创建适配器
  const adapter = createXiaoweiAdapter({
    coreWsUrl: 'ws://localhost:8001/ws',
    authToken: 'your-token'
  });

  // 连接
  await adapter.connect({
    onConnect: () => console.log('已连接'),
    onError: (err) => console.error('错误:', err)
  });

  try {
    // 1. 查询配置
    const configResponse = await adapter.config.queryConfig({
      keys: ['app.*']
    });
    console.log('配置:', configResponse.data);

    // 2. 获取工作台建议
    const suggestions = await adapter.workbench.getSuggestions({
      currentPage: '/config',
      userRole: 'admin'
    });
    console.log('建议:', suggestions.data);

    // 3. 验证用户
    const authResponse = await adapter.auth.verifyAuth({
      userId: 'user123',
      type: 'session'
    });
    console.log('认证结果:', authResponse.data);

    // 4. 查询用户
    const users = await adapter.user.queryUsers({
      filters: { status: 'active' }
    });
    console.log('用户列表:', users.data?.users);

  } catch (error) {
    console.error('操作失败:', error);
  } finally {
    // 断开连接
    adapter.disconnect();
  }
}

main();
```

---

**文档更新时间**: 2026-03-26  
**维护者**: 玄玑引擎团队
