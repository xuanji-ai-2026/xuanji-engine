# 玄玑引擎用户端 (User Client)

玄玑引擎用户端应用 - 基于React + TypeScript + Vite的现代化前端应用

## 技术栈

- **React 18.3.1** - UI框架
- **TypeScript 5.9.3** - 类型安全的JavaScript
- **Vite 5.3.1** - 现代化构建工具
- **Zustand 4.4.0** - 轻量级状态管理
- **Tailwind CSS 3.4.3** - 实用优先的CSS框架
- **React Router 6.20.0** - 路由管理
- **React Query 5.0.0** - 数据获取和缓存
- **React Hook Form 7.48.0** - 表单管理
- **Zod 3.22.0** - 数据验证

## 项目结构

```
src/
├── assets/              # 静态资源
├── components/          # 组件
│   ├── auth/           # 认证组件
│   ├── common/         # 通用组件
│   └── layout/         # 布局组件
├── config/             # 配置文件
├── hooks/              # 自定义Hooks
├── layouts/            # 布局
├── pages/              # 页面组件
│   ├── auth/           # 认证页面
│   ├── user/           # 用户页面
│   ├── authorization/  # 授权管理页面
│   ├── smart-config/   # 智能配置页面
│   ├── auto-generate/  # 自动配置生成页面
│   ├── digital-human/  # 数字人管理页面
│   ├── chat/           # 对话页面
│   ├── plugin-market/  # 插件市场页面
│   ├── billing/        # 计费中心页面
│   └── assistant/      # 智能助手页面
├── services/           # API服务
├── stores/             # Zustand状态管理
├── types/              # TypeScript类型定义
├── utils/              # 工具函数
├── App.tsx             # 根组件
├── main.tsx            # 入口文件
└── index.css           # 全局样式
```

## 核心模块

### 1. 用户认证授权 (35个功能点)
- ✅ 用户注册
- ✅ 用户登录
- ✅ 忘记密码
- ✅ 重置密码
- ✅ 用户信息管理
- ✅ Token刷新
- ✅ 登出功能
- ✅ 邮箱验证
- ✅ 发送验证码

### 2. 授权管理 (20个功能点)
- ✅ 工作人员管理
- ✅ 角色管理
- ✅ 权限管理
- ✅ 权限检查
- ✅ 用户权限查询

### 3. 智能配置 (40个功能点)
- ✅ 多轮对话配置
- ✅ 配置会话管理
- ✅ 配置历史记录
- ✅ 配置模板管理
- ✅ 流式对话
- ✅ 配置建议

### 4. 自动配置生成 (30个功能点)
- ✅ 人格配置
- ✅ 情绪配置
- ✅ 插件配置
- ✅ 知识库配置
- ✅ 配置向导

### 5. 数字人管理 (20个功能点)
- ✅ 数字人列表
- ✅ 创建数字人
- ✅ 数字人详情
- ✅ 更新数字人
- ✅ 删除数字人
- ✅ 启动/停止数字人
- ✅ 克隆数字人
- ✅ 数字人模板

### 6. 对话交互 (20个功能点)
- ✅ 对话列表
- ✅ 创建对话
- ✅ 发送消息
- ✅ 流式消息
- ✅ 对话历史
- ✅ 语音输入
- ✅ 文字转语音

### 7. 插件市场 (10个功能点)
- ✅ 插件列表
- ✅ 插件搜索
- ✅ 安装插件
- ✅ 我的插件
- ✅ 插件评论

### 8. 计费中心 (20个功能点)
- ✅ 账户概览
- ✅ 充值功能
- ✅ 账单管理
- ✅ 发票管理
- ✅ 交易记录
- ✅ 套餐订阅

### 9. 智能助手小紫 (10个功能点)
- ✅ 对话功能
- ✅ 语音交互
- ✅ 新手引导
- ✅ 快捷操作
- ✅ 智能推荐

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

### 类型检查

```bash
npm run type-check
```

### 代码检查

```bash
npm run lint
```

## 环境变量

创建 `.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_BASE_URL=ws://localhost:5000
```

## 核心功能说明

### 状态管理 (Zustand)

项目使用Zustand进行状态管理，主要Store包括：

- `authStore` - 用户认证状态
- `digitalHumanStore` - 数字人状态
- `chatStore` - 对话状态
- `assistantStore` - 智能助手状态
- `themeStore` - 主题和设置状态
- `globalStore` - 全局状态（通知、在线状态等）

### API服务

所有API调用通过Service层封装：

- `authService` - 认证服务
- `authorizationService` - 授权服务
- `digitalHumanService` - 数字人服务
- `chatService` - 对话服务
- `pluginService` - 插件服务
- `billingService` - 计费服务
- `smartConfigService` - 智能配置服务
- `assistantService` - 智能助手服务

### 路由配置

使用React Router进行路由管理，支持：

- 公开路由（登录、注册等）
- 受保护路由（需要认证）
- 嵌套路由（带布局）

### 主题系统

支持三种主题模式：
- Light（浅色）
- Dark（深色）
- Auto（自动跟随系统）

### 响应式设计

完全响应式设计，支持：
- 桌面端（>= 1024px）
- 平板端（768px - 1023px）
- 移动端（< 768px）

## TypeScript配置

项目使用TypeScript严格模式，确保类型安全：

```json
{
  "strict": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true,
  "noFallthroughCasesInSwitch": true
}
```

## 代码规范

- 使用函数式组件 + Hooks
- 所有组件使用TypeScript类型
- 遵循React最佳实践
- 使用ESLint进行代码检查

## 构建优化

Vite构建优化：
- 代码分割
- 懒加载
- Tree-shaking
- 压缩优化

## 浏览器支持

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)

## 开发注意事项

1. 所有组件使用TypeScript编写
2. 使用Zustand进行状态管理
3. API调用通过Service层封装
4. 表单使用React Hook Form
5. 样式使用Tailwind CSS
6. 使用相对路径导入（@别名）

## 许可证

MIT License

## 联系方式

如有问题，请联系开发团队。
