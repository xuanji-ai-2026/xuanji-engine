# 快速启动指南

## 前置要求

确保已安装以下工具：
- Node.js >= 18.0.0
- npm >= 9.0.0 或 yarn >= 1.22.0

## 安装步骤

### 1. 进入项目目录
```bash
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/admin-console
```

### 2. 安装依赖
```bash
npm install
```

### 3. 启动开发服务器
```bash
npm run dev
```

### 4. 访问应用
打开浏览器访问: http://localhost:3000

## 测试账号

- 邮箱: `admin@xuanji.ai`
- 密码: `123456`

## 可用脚本

### 开发
```bash
npm run dev          # 启动开发服务器
npm run type-check   # TypeScript 类型检查
npm run lint         # ESLint 代码检查
```

### 构建
```bash
npm run build        # 构建生产版本
npm run preview      # 预览生产构建
```

## 项目结构快速浏览

```
admin-console/
├── src/
│   ├── components/     # 公共组件
│   │   ├── Header.tsx
│   │   └── Sidebar.tsx
│   ├── pages/          # 页面组件
│   │   ├── Assistant/     # 智能助手
│   │   ├── DigitalHumans/ # 数字人
│   │   ├── Knowledge/     # 知识源
│   │   ├── Operations/    # 运营
│   │   ├── Plugins/       # 插件
│   │   ├── Settings/      # 配置
│   │   ├── SystemInit/    # 初始化
│   │   ├── Updates/       # 更新
│   │   └── Users/         # 用户
│   ├── stores/        # 状态管理
│   ├── hooks/         # 自定义 Hooks
│   ├── utils/         # 工具函数
│   └── types/         # 类型定义
├── package.json
├── README.md
└── PROJECT_OVERVIEW.md
```

## 核心功能模块

### 1. 仪表板（Dashboard）
- 系统概览
- 快速统计
- 快捷操作

### 2. 系统初始化（SystemInit）
- 一键创世
- 创始人绑定
- 隐身激活

### 3. 用户管理（Users）
- 用户列表
- 用户详情
- 权限管理
- 搜索筛选

### 4. 数字人管理（DigitalHumans）
- 数字人列表
- 配置管理
- 使用统计

### 5. 知识源管理（Knowledge）
- 知识源列表
- 数据同步
- 统计分析

### 6. 插件管理（Plugins）
- 插件列表
- 审核管理
- 统计报表

### 7. 运营管理（Operations）
- 运营概览
- 系统维护
- 安全管理
- 数据分析

### 8. UI配置（Settings）
- 主题设置
- 布局配置
- 动画配置
- LOGO设置

### 9. 更新管理（Updates）
- 版本更新
- 版本历史
- 公告管理
- 插件推荐

### 10. 智能助手小灵（Assistant）
- 系统监控
- 异常预警
- 决策建议
- 告警管理

## 常见问题

### Q: 端口 3000 被占用怎么办？
A: 修改 `vite.config.ts` 中的 `server.port` 配置

### Q: 如何切换到暗黑模式？
A: 点击右上角的月亮/太阳图标切换主题

### Q: 如何添加新页面？
A: 在 `src/pages/` 下创建新组件，然后在 `src/router/index.tsx` 中添加路由

### Q: 如何修改 API 地址？
A: 修改 `vite.config.ts` 中的 `proxy.target` 配置

### Q: 如何添加新的状态管理？
A: 在 `src/stores/` 下创建新的 store 文件，使用 Zustand API

## 开发建议

1. **遵循代码规范**
   - 使用 TypeScript 严格模式
   - 函数式组件优先
   - 使用自定义 Hooks

2. **性能优化**
   - 使用 React.memo 优化组件
   - 合理使用 useMemo 和 useCallback
   - 大列表使用虚拟滚动

3. **代码组织**
   - 每个功能模块独立目录
   - 公共组件放在 components
   - 复用逻辑封装成 Hooks

## 调试技巧

### React DevTools
安装 React DevTools 浏览器扩展，可以查看组件树和状态

### Redux DevTools
Zustand 支持 Redux DevTools，可以在浏览器中查看状态变化

### Console 日志
使用 `console.log()` 调试代码，生产环境会自动移除

### 网络请求
使用浏览器 Network 面板查看 API 请求

## 构建部署

### 构建生产版本
```bash
npm run build
```

### 部署到服务器
将 `dist/` 目录上传到服务器，配置 Nginx 指向该目录

### 环境变量
创建 `.env.production` 文件配置生产环境变量

## 技术支持

如有问题，请查看：
- README.md - 完整文档
- PROJECT_OVERVIEW.md - 项目概览
- 代码注释 - 代码说明

## 下一步

1. 熟悉项目结构
2. 查看核心组件代码
3. 了解状态管理
4. 尝试修改页面样式
5. 添加新功能模块

祝您使用愉快！🎉
