# 小微适配层架构文档

**版本**: v1.0.0  
**描述**: 小微适配层的系统架构设计

---

## 目录

- [架构概览](#架构概览)
- [模块设计](#模块设计)
- [通信流程](#通信流程)
- [数据流](#数据流)
- [错误处理](#错误处理)
- [安全设计](#安全设计)
- [扩展性设计](#扩展性设计)

---

## 架构概览

### 系统分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                        配置端应用层                           │
│         (React / Vue / Angular / Native / Other)              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ API 调用
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     小微适配层                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    统一入口                              │ │
│  │              (XiaoweiAdapter / createXiaoweiAdapter)   │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   配置模块                               │ │
│  │           (ConfigAdapter + ConfigService)                │ │
│  │  - 查询配置                                              │ │
│  │  - 修改配置                                              │ │
│  │  - 验证配置                                              │ │
│  │  - 批量操作                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   工作台模块                             │ │
│  │         (WorkbenchHelper + WorkbenchService)             │ │
│  │  - 流程引导                                              │ │
│  │  - 操作建议                                              │ │
│  │  - 导入导出                                              │ │
│  │  - 批量管理                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   认证模块                               │ │
│  │             (AuthHelper + AuthService)                   │ │
│  │  - 用户认证                                              │ │
│  │  - 权限管理                                              │ │
│  │  - 安全检查                                              │ │
│  │  - 会话管理                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   用户管理模块                           │ │
│  │            (UserHelper + UserService)                    │ │
│  │  - 用户查询                                              │ │
│  │  - 用户配置                                              │ │
│  │  - 批量操作                                              │ │
│  │  - 统计信息                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ WebSocket Message
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   传输层 (WebSocket)                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           ConnectionManager (连接管理)                  │ │
│  │  - 自动连接                                              │ │
│  │  - 断线重连                                              │ │
│  │  - 心跳检测                                              │ │
│  │  - 消息队列                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │          MessageDispatcher (消息分发)                    │ │
│  │  - 消息路由                                              │ │
│  │  - 响应匹配                                              │ │
│  │  - 超时处理                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ WebSocket Protocol
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 紫微元灵核心                                 │
│            (Ziwei Star Core - Python)                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              意图理解模块                               │ │
│  │      (IntentUnderstanding / IntentRecognizer)           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              智能推理模块                               │ │
│  │          (SelfEvolution / IntentDriftDetector)           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              多模态处理模块                             │ │
│  │          (MultimodalIntentRecognizer)                    │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              行业模板模块                               │ │
│  │             (IndustryTemplate)                          │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 关键设计原则

1. **分层解耦**: 各层职责明确，易于维护和扩展
2. **统一接口**: 对外提供统一的 API 接口，隐藏内部实现细节
3. **异步非阻塞**: 所有操作都是异步的，不阻塞主线程
4. **类型安全**: 使用 TypeScript 确保类型安全
5. **错误可追踪**: 完善的错误处理和日志机制
6. **自动重连**: WebSocket 断线自动重连，提高可用性

---

## 模块设计

### 1. 统一入口模块 (XiaoweiAdapter)

**职责**:
- 提供工厂函数 `createXiaoweiAdapter`
- 统一管理所有子模块
- 处理连接生命周期

**接口**:
```typescript
class XiaoweiAdapter {
  connect(events?: WebSocketEvents): Promise<void>
  disconnect(): void
  get config: ConfigAdapter
  get workbench: WorkbenchHelper
  get auth: AuthHelper
  get user: UserHelper
}
```

### 2. 配置模块 (ConfigAdapter)

**职责**:
- 配置项查询
- 配置项修改
- 配置验证
- 批量配置操作

**核心方法**:
```typescript
queryConfig(params: ConfigQueryParams): Promise<BaseResponse<ConfigItem[]>>
modifyConfig(params: ConfigModifyParams): Promise<BaseResponse<...>>
validateConfig(configs: Record<string, any>): Promise<BaseResponse<ValidationResult>>
batchConfig(operations: BatchConfigOperation[]): Promise<BaseResponse<any>>
```

### 3. 工作台模块 (WorkbenchHelper)

**职责**:
- 提供工作台流程引导
- 生成快速操作建议
- 批量配置管理
- 配置导入/导出

**核心方法**:
```typescript
getGuide(taskType: string): Promise<BaseResponse<WorkbenchGuide>>
getSuggestions(context: object): Promise<BaseResponse<WorkbenchSuggestion[]>>
exportConfigs(format: string): Promise<BaseResponse<{ data: string; filename: string }>>
importConfigs(data: string, format: string): Promise<BaseResponse<{ imported: number }>>
```

### 4. 认证模块 (AuthHelper)

**职责**:
- 用户认证
- 权限管理
- 安全检查
- 会话管理

**核心方法**:
```typescript
verifyAuth(params: AuthVerifyParams): Promise<BaseResponse<AuthResult>>
configureAuth(params: AuthConfigureParams): Promise<BaseResponse<{ success: boolean }>>
performSecurityCheck(): Promise<BaseResponse<SecurityCheckResult>>
checkPermission(userId: string, permission: string): Promise<BaseResponse<{ granted: boolean }>>
```

### 5. 用户管理模块 (UserHelper)

**职责**:
- 用户信息查询
- 用户配置管理
- 批量用户操作
- 用户统计信息

**核心方法**:
```typescript
queryUsers(params: UserQueryParams): Promise<BaseResponse<{ users: UserInfo[]; total: number }>>
configureUser(params: UserConfigureParams): Promise<BaseResponse<UserInfo>>
batchUserOperations(operations: BatchUserOperation[]): Promise<BaseResponse<...>>
getUserStatistics(): Promise<BaseResponse<UserStatistics>>
```

---

## 通信流程

### 1. 连接建立流程

```
应用层              小微适配层            WebSocket            紫微元灵核心
  │                    │                   │                      │
  │  connect()         │                   │                      │
  ├──────────────────>│                   │                      │
  │                    │  new WebSocket()  │                      │
  │                    ├──────────────────>│                      │
  │                    │                   │  CONNECT            │
  │                    │                   ├────────────────────>│
  │                    │                   │                      │
  │                    │                   │  CONNECT ACK         │
  │                    │                   │<────────────────────┤
  │                    │  onopen           │                      │
  │  onConnect         │<──────────────────┤                      │
  │<───────────────────┤                   │                      │
```

### 2. 消息请求-响应流程

```
应用层              小微适配层            WebSocket            紫微元灵核心
  │                    │                   │                      │
  │  queryConfig()     │                   │                      │
  ├──────────────────>│                   │                      │
  │                    │  生成 Message ID  │                      │
  │                    │  注册回调        │                      │
  │                    │                   │  SEND Message        │
  │                    ├──────────────────>│                      │
  │                    │                   │  PROCESS             │
  │                    │                   ├────────────────────>│
  │                    │                   │                      │
  │                    │                   │  RESPONSE            │
  │                    │                   │<────────────────────┤
  │                    │  onmessage        │                      │
  │                    │<──────────────────┤                      │
  │                    │  匹配 Message ID  │                      │
  │                    │  调用回调        │                      │
  │  Response          │                   │                      │
  │<───────────────────┤                   │                      │
```

### 3. 断线重连流程

```
应用层              小微适配层            WebSocket            紫微元灵核心
  │                    │                   │                      │
  │                    │  onclose          │                      │
  │  onDisconnect      │<──────────────────┤                      │
  │<───────────────────┤                   │                      │
  │                    │  等待 delay      │                      │
  │                    │                   │                      │
  │                    │  setTimeout       │                      │
  │                    │  ──────────────>  │                      │
  │                    │                   │                      │
  │                    │  reconnect()      │                      │
  │                    │  new WebSocket()  │                      │
  │                    ├──────────────────>│                      │
  │                    │                   │  CONNECT            │
  │                    │                   ├────────────────────>│
  │                    │                   │                      │
```

---

## 数据流

### 1. 配置查询数据流

```
Input: ConfigQueryParams
  ↓
Validation (keys, group)
  ↓
Construct Message (id, type: CONFIG_QUERY, payload)
  ↓
Send via WebSocket
  ↓
Ziwei Core Process
  ↓
Query Config Store
  ↓
Filter Configs
  ↓
Construct Response
  ↓
Send via WebSocket
  ↓
Receive Message
  ↓
Parse Response
  ↓
Return BaseResponse<ConfigItem[]>
```

### 2. 配置修改数据流

```
Input: ConfigModifyParams
  ↓
Validation (items, validate)
  ↓
If validate:
  ↓
  Call validateConfig()
  ↓
  Check ValidationResult.valid
  ↓
  If invalid: Return errors
  ↓
Construct Message (id, type: CONFIG_MODIFY, payload)
  ↓
Send via WebSocket
  ↓
Ziwei Core Process
  ↓
Validate Each Config
  ↓
Apply Changes
  ↓
If persist: Save to Store
  ↓
Construct Response (success, updated keys)
  ↓
Send via WebSocket
  ↓
Return BaseResponse<{ success, updated }>
```

---

## 错误处理

### 错误分类

1. **网络错误**: WebSocket 连接失败、断线
2. **超时错误**: 消息响应超时
3. **验证错误**: 配置验证失败
4. **权限错误**: 无权限操作
5. **业务错误**: 紫微元灵核心返回的业务错误

### 错误处理策略

```typescript
// 1. 网络错误 - 自动重连
ws.onerror = (error) => {
  log('WebSocket error:', error);
  triggerReconnect();
};

// 2. 超时错误 - 返回超时异常
const timeout = setTimeout(() => {
  reject(new Error(`Message timeout: ${messageId}`));
}, this.config.timeout);

// 3. 验证错误 - 返回详细信息
if (!validationResult.valid) {
  return {
    status: 'error',
    error: 'Config validation failed',
    data: validationResult
  };
}

// 4. 业务错误 - 统一格式
if (response.status === 'error') {
  throw new AdapterError(response.error, response.code);
}
```

### 错误传播

```
Application
  ↓ try/catch
Adapter API
  ↓ try/catch
WebSocket Handler
  ↓ error event
Connection Manager
  ↓ reconnect attempt
  ↓
Application Error Handler
```

---

## 安全设计

### 1. 认证机制

```
连接阶段:
  1. 应用提供 authToken
  2. 连接时发送认证信息
  3. 紫微元灵核心验证 Token
  4. 建立安全会话

请求阶段:
  1. 每个消息包含用户标识
  2. 紫微元灵核心验证权限
  3. 操作审计日志
```

### 2. 权限控制

```typescript
// 权限检查
async checkPermission(userId: string, permission: string) {
  // 1. 查询用户角色
  const user = await getUserById(userId);
  
  // 2. 查询角色权限
  const permissions = await getPermissions(user.role);
  
  // 3. 检查是否有权限
  const granted = permissions.includes(permission);
  
  // 4. 记录审计日志
  await logAudit({
    userId,
    permission,
    granted,
    timestamp: Date.now()
  });
  
  return { granted };
}
```

### 3. 数据安全

- **敏感数据加密**: 传输层使用 TLS
- **配置数据脱敏**: 返回响应时隐藏敏感字段
- **审计日志**: 记录所有关键操作

### 4. 安全检查

```typescript
// 安全检查项
- 密码策略 (最小长度、复杂度)
- 会话超时配置
- Token 轮换机制
- SSL/TLS 配置
- IP 白名单
```

---

## 扩展性设计

### 1. 插件机制

```typescript
// 插件接口
interface AdapterPlugin {
  name: string;
  version: string;
  install(adapter: XiaoweiAdapter): void;
  uninstall(adapter: XiaoweiAdapter): void;
}

// 注册插件
adapter.registerPlugin(new AuditPlugin());
adapter.registerPlugin(new CachePlugin());
```

### 2. 中间件机制

```typescript
// 中间件
interface Middleware {
  before(message: Message): Promise<Message>;
  after(response: BaseResponse): Promise<BaseResponse>;
}

// 应用中间件
adapter.use(new LoggingMiddleware());
adapter.use(new CacheMiddleware());
adapter.use(new MetricsMiddleware());
```

### 3. 自定义消息处理器

```typescript
// 注册自定义消息处理器
adapter.on('custom.message', async (payload) => {
  // 处理自定义消息
  return {
    status: 'success',
    data: { result: 'processed' }
  };
});
```

---

## 性能优化

### 1. 连接池

```
- 复用 WebSocket 连接
- 避免频繁建立/断开连接
- 连接健康检查
```

### 2. 消息队列

```
- 请求队列管理
- 并发控制
- 优先级队列
```

### 3. 缓存策略

```
- 配置缓存
- 用户信息缓存
- TTL 过期策略
```

### 4. 批量操作

```
- 合并多个小请求为大请求
- 减少网络往返次数
- 提高吞吐量
```

---

**文档维护**: 玄玑引擎团队  
**最后更新**: 2026-03-26
