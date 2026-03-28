# 玄玑引擎开发者端 (Developer Client)

玄玑引擎开发者端应用，提供完整的API管理、插件开发、SDK集成和AI助手功能。

## 技术栈

- **React 18.3.1** - UI框架
- **TypeScript 5.9.3** - 类型安全
- **Vite 5.3.1** - 构建工具
- **Zustand 4.4.0** - 状态管理
- **Tailwind CSS 3.4.3** - 样式框架
- **React Router DOM 6.22.0** - 路由管理
- **Monaco Editor** - 代码编辑器
- **Recharts** - 数据可视化

## 功能模块

### 1. API管理 (20个功能点)
- ✅ 密钥列表显示
- ✅ 密钥创建
- ✅ 密钥编辑
- ✅ 密钥删除
- ✅ 密钥撤销
- ✅ 权限配置
- ✅ 调用统计概览
- ✅ 调用量趋势图
- ✅ 成本统计
- ✅ 错误率统计
- ✅ 成功率统计
- ✅ 接口调试工具
- ✅ 请求构建
- ✅ 响应预览
- ✅ 调试历史
- ✅ API文档查看
- ✅ API搜索
- ✅ 示例代码生成
- ✅ 在线测试
- ✅ 错误码查询

### 2. 插件开发 (30个功能点)
- ✅ 插件列表
- ✅ 插件创建向导
- ✅ 插件代码编辑器 (Monaco)
- ✅ 插件配置界面
- ✅ 插件依赖管理
- ✅ 插件测试环境
- ✅ 单元测试
- ✅ 集成测试
- ✅ 性能测试
- ✅ 插件调试
- ✅ 日志查看
- ✅ 测试结果展示
- ✅ 代码覆盖率
- ✅ 插件打包
- ✅ 插件上架申请
- ✅ 审核状态查看
- ✅ 版本管理
- ✅ 插件模板
- ✅ 常用代码片段
- ✅ 智能代码补全
- ✅ 代码质量检查
- ✅ 文档生成
- ✅ 示例演示
- ✅ 插件市场浏览
- ✅ 插件搜索
- ✅ 插件安装
- ✅ 插件卸载
- ✅ 插件更新
- ✅ 依赖检查
- ✅ 兼容性检测

### 3. SDK管理 (20个功能点)
- ✅ SDK列表展示
- ✅ SDK下载
- ✅ 版本信息展示
- ✅ 多平台支持
- ✅ 集成文档
- ✅ 快速开始指南
- ✅ 分步教程
- ✅ 代码示例
- ✅ 版本更新日志
- ✅ 更新历史查询
- ✅ 文件大小显示
- ✅ 发布日期
- ✅ 在线代码预览
- ✅ 代码高亮
- ✅ 代码复制
- ✅ 多语言支持
- ✅ 基础用法示例
- ✅ 高级功能示例
- ✅ 错误处理示例
- ✅ 配置参考

### 4. 智能助手小元 (10个功能点)
- ✅ 对话式AI助手
- ✅ 代码生成
- ✅ 功能描述转代码
- ✅ 多语言支持
- ✅ 错误诊断
- ✅ 错误分析
- ✅ 修复建议
- ✅ 代码优化
- ✅ 性能优化建议
- ✅ 最佳实践推荐

## 项目结构

```
src/
├── components/       # 通用组件
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   ├── Modal.tsx
│   ├── Toast.tsx
│   ├── Badge.tsx
│   ├── Tabs.tsx
│   └── Layout.tsx
├── hooks/           # 自定义Hooks
│   ├── useLocalStorage.ts
│   ├── useDebounce.ts
│   └── useCopyToClipboard.ts
├── pages/           # 页面组件
│   ├── api/        # API管理模块
│   ├── plugin/     # 插件开发模块
│   ├── sdk/        # SDK管理模块
│   ├── assistant/  # 智能助手模块
│   └── common/     # 通用页面
├── services/       # API服务
│   ├── api.ts
│   ├── plugin.ts
│   ├── sdk.ts
│   └── assistant.ts
├── stores/         # Zustand状态管理
│   ├── apiStore.ts
│   ├── pluginStore.ts
│   ├── sdkStore.ts
│   ├── assistantStore.ts
│   └── appStore.ts
├── styles/         # 样式文件
│   └── index.css
├── types/          # TypeScript类型定义
│   └── index.ts
├── utils/          # 工具函数
│   ├── index.ts
│   └── request.ts
├── App.tsx
└── main.tsx
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 环境变量

创建 `.env` 文件：

```env
VITE_API_BASE_URL=/api/v1
```

## 开发规范

### TypeScript
- 使用严格模式
- 所有组件必须有类型定义
- 使用函数式组件 + Hooks

### 代码风格
- 使用Tailwind CSS进行样式
- 组件使用PascalCase命名
- 工具函数使用camelCase命名
- 常量使用UPPER_SNAKE_CASE命名

### Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
perf: 性能优化
test: 测试相关
chore: 构建/工具链相关
```

## 浏览器支持

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)

## 许可证

MIT
