# 快速开始指南

## 🚀 5分钟快速启动

### 1. 安装依赖

```bash
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/config-client
pnpm install
```

### 2. 启动开发服务器

```bash
pnpm run dev
```

### 3. 访问应用

打开浏览器访问: http://localhost:3000

### 4. 登录系统

使用默认账号登录：
- 用户名: `admin`
- 密码: `admin123`

## 📁 项目结构概览

```
config-client/
├── src/
│   ├── components/      # 通用组件（按钮、卡片等）
│   ├── pages/          # 页面（登录、仪表盘）
│   ├── modules/        # 业务模块（认证、配置等）
│   ├── stores/         # 状态管理
│   ├── hooks/          # 自定义Hooks
│   ├── utils/          # 工具函数
│   └── types/          # TypeScript类型
├── public/             # 静态资源
└── 配置文件
```

## 🎯 核心功能导航

登录后可访问以下功能模块：

| 路径 | 模块 | 描述 |
|------|------|------|
| `/` | 工作台 | 系统概览和快捷操作 |
| `/auth` | 认证协助 | 认证请求管理 |
| `/config` | 配置协助 | 配置请求管理 |
| `/workbench` | 任务管理 | 任务和待办管理 |
| `/assistant` | 智能助手 | AI助手对话 |
| `/user` | 用户管理 | 用户和权限管理 |

## 💡 常用命令

```bash
# 开发模式
pnpm run dev

# 构建生产版本
pnpm run build

# 预览生产版本
pnpm run preview

# 类型检查
pnpm run type-check

# 代码检查
pnpm run lint
```

## 🔧 环境配置

复制 `.env.example` 为 `.env` 并配置：

```bash
VITE_API_BASE_URL=/api
VITE_APP_TITLE=玄玑引擎配置端
VITE_ENV=development
```

## 📚 查看更多文档

- [README.md](./README.md) - 完整的项目文档
- [DELIVERY.md](./DELIVERY.md) - 项目交付说明
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - 详细的功能清单

## ❓ 常见问题

### Q: 如何添加新的业务模块？
A: 在 `src/modules/` 下创建新目录，参考现有模块结构。

### Q: 如何修改主题颜色？
A: 编辑 `tailwind.config.js` 中的 `theme.extend.colors`。

### Q: 如何集成后端API？
A: 修改 `.env` 中的 `VITE_API_BASE_URL`，确保API返回正确的数据格式。

### Q: TypeScript报错怎么办？
A: 运行 `pnpm run type-check` 查看具体错误，大部分是类型定义问题。

## 🎨 自定义样式

所有样式使用Tailwind CSS，参考文档：https://tailwindcss.com/docs

## 🔗 技术文档

- [React](https://react.dev)
- [TypeScript](https://www.typescriptlang.org/docs)
- [Vite](https://vitejs.dev)
- [Zustand](https://zustand-demo.pmnd.rs)
- [Tailwind CSS](https://tailwindcss.com)

---

祝你开发愉快！🎉
