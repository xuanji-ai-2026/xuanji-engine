# UI模板配置模块

## 模块信息

- **版本**: v2.0
- **负责人**: 康辅星 (162)
- **负责组**: 辅弼星辰组
- **优先级**: P1
- **预计工时**: 80小时
- **状态**: 已完成

## 功能概述

UI模板配置模块提供完整的UI定制化解决方案，支持通过后台配置LOGO、背景、启动动画、主题和布局，无需修改代码即可实现UI定制。

## 核心功能

### 1. LOGO管理 (logo_manager.py)
- 支持PNG、JPG、SVG、WebP格式
- 支持亮色/暗色主题LOGO
- 支持自动调整尺寸
- 支持设置默认LOGO

### 2. 背景管理 (background_manager.py)
- 支持多页面背景配置（登录页、仪表盘等）
- 支持多种显示模式（cover、contain、stretch、tile）
- 自动生成缩略图
- 支持背景尺寸和比例信息

### 3. 动画管理 (animation_manager.py)
- 支持GIF、Lottie、MP4、WebM格式
- 支持启动动画、加载动画、过渡动画
- 支持Lottie动画解析
- 支持程序化生成Lottie动画

### 4. 主题管理 (theme_manager.py)
- 内置默认、亮、暗色、紧凑主题
- 支持自定义主题创建
- 支持主题复制/继承
- 自动生成CSS变量
- 主题颜色格式验证

### 5. 布局管理 (layout_manager.py)
- 内置多种布局模板（默认、宽屏、紧凑、右侧边栏、顶部导航）
- 支持自定义布局创建
- 支持侧边栏、头部、底部、内容区配置
- 响应式断点支持
- 布局预览功能

### 6. RESTful API (ui_template_api.py)
提供40+ RESTful API接口，支持所有功能的后台操作。

## 文件结构

```
10_fubi_star/src/
├── ui_template_config.py    # 核心配置管理器
├── logo_manager.py          # LOGO管理器
├── background_manager.py     # 背景管理器
├── animation_manager.py      # 动画管理器
├── theme_manager.py          # 主题管理器
├── layout_manager.py         # 布局管理器
├── ui_template_api.py        # RESTful API接口
└── ui_template_test.py       # 单元测试
```

## 快速开始

### 基本使用

```python
import asyncio
from ui_template_config import UITemplateConfig
from logo_manager import LogoManager
from theme_manager import ThemeManager

async def main():
    # 初始化配置管理器
    config = UITemplateConfig()

    # 获取配置
    logo_width = await config.get_config("logo.width")
    print(f"LOGO宽度: {logo_width}")

    # 修改配置
    await config.set_config("logo.width", 300)

    # LOGO管理
    logo_manager = LogoManager()
    result = await logo_manager.upload_logo(
        file_data=b"...",
        filename="logo.png",
        theme="light"
    )

    # 主题管理
    theme_manager = ThemeManager()
    themes = await theme_manager.list_themes()
    print(f"可用主题: {themes['total']}")

    await theme_manager.set_current_theme("dark")

asyncio.run(main())
```

### 使用API

```python
from ui_template_api import UITemplateAPI

async def main():
    api = UITemplateAPI()

    # 获取所有配置
    all_config = await api.api_get_all_configs()

    # 创建新主题
    colors = {
        "primary": "#ff6b6b",
        "secondary": "#4ecdc4"
    }
    result = await api.api_create_theme(
        theme_id="custom",
        name="自定义主题",
        description="我的自定义主题",
        colors=colors
    )

asyncio.run(main())
```

## API文档

### 核心配置API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/ui_templates/config` | 获取配置 |
| PUT | `/api/ui_templates/config` | 设置配置 |
| PATCH | `/api/ui_templates/config` | 批量更新配置 |
| POST | `/api/ui_templates/config/reset` | 重置配置 |
| GET | `/api/ui_templates/config/validate` | 验证配置 |
| GET | `/api/ui_templates/config/export` | 导出配置 |
| POST | `/api/ui_templates/config/import` | 导入配置 |

### LOGO管理API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ui_templates/logo/upload` | 上传LOGO |
| GET | `/api/ui_templates/logo` | 列出所有LOGO |
| GET | `/api/ui_templates/logo/{id}` | 获取LOGO信息 |
| DELETE | `/api/ui_templates/logo/{id}` | 删除LOGO |
| POST | `/api/ui_templates/logo/default` | 设置默认LOGO |
| GET | `/api/ui_templates/logo/default/{theme}` | 获取默认LOGO |

### 背景管理API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ui_templates/background/upload` | 上传背景 |
| GET | `/api/ui_templates/background` | 列出所有背景 |
| GET | `/api/ui_templates/background/{id}` | 获取背景信息 |
| DELETE | `/api/ui_templates/background/{id}` | 删除背景 |
| POST | `/api/ui_templates/background/set` | 设置页面背景 |
| GET | `/api/ui_templates/background/page/{page}` | 获取页面背景 |

### 动画管理API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ui_templates/animation/upload` | 上传动画 |
| GET | `/api/ui_templates/animation` | 列出所有动画 |
| GET | `/api/ui_templates/animation/{id}` | 获取动画信息 |
| DELETE | `/api/ui_templates/animation/{id}` | 删除动画 |
| POST | `/api/ui_templates/animation/set` | 设置动画 |
| GET | `/api/ui_templates/animation/config/{type}` | 获取动画配置 |
| POST | `/api/ui_templates/animation/lottie` | 创建Lottie动画 |

### 主题管理API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ui_templates/theme` | 创建主题 |
| GET | `/api/ui_templates/theme` | 列出所有主题 |
| GET | `/api/ui_templates/theme/{id}` | | 获取主题 |
| PUT | `/api/ui_templates/theme/{id}` | 更新主题 |
| DELETE | `/api/ui_templates/theme/{id}` | 删除主题 |
| POST | `/api/ui_templates/theme/current` | 设置当前主题 |
| GET | `/api/ui_templates/theme/current` | 获取当前主题 |
| GET | `/api/ui_templates/theme/{id}/css` | 获取CSS变量 |
| GET | `/api/ui_templates/theme/{id}/preview` | 获取主题预览 |
| POST | `/api/ui_templates/theme/duplicate` | 复制主题 |

### 布局管理API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ui_templates/layout` | 创建布局 |
| GET | `/api/ui_templates/layout` | 列出所有布局 |
| GET | `/api/ui_templates/layout/{id}` | 获取布局 |
| PUT | `/api/ui_templates/layout/{id}` | 更新布局 |
| DELETE | `/api/ui_templates/layout/{id}` | 删除布局 |
| POST | `/api/ui_templates/layout/current` | 设置当前布局 |
| GET | `/api/ui_templates/layout/current` | 获取当前布局 |
| GET | `/api/ui_templates/layout/{id}/preview` | 预览布局 |
| POST | `/api/ui_templates/layout/duplicate` | 复制布局 |

### 综合API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/ui_templates/all`` | 获取所有配置 |
| GET | `/api/ui_templates/status` | 获取系统状态 |

## 运行测试

```bash
cd /workspace/projects/workspace/xuanji-engine-v2/backend/10_fubi_star/src
python ui_template_test.py
```

## 依赖项

- Python 3.8+
- Pillow (PIL)
- 标准库: json, asyncio, pathlib, datetime, hashlib, shutil, copy, re, io, tempfile

## 配置存储

所有配置文件存储在以下目录结构：

```
configs/
├── ui_templates/
│   ├── ui_templates.json    # 主配置文件
├── themes/
│   ├── themes.json          # 主题定义
│   └── theme_config.json    # 当前主题配置
└── layouts/
    ├── layouts.json         # 布局定义
    └── layout_config.json   # 当前布局配置

storage/
├── logos/                   # LOGO文件
├── backgrounds/
│   └── thumbnails/          # 背景缩略图
└── animations/
    └── metadata.json         # 动画元数据
```

## 安全考虑

1. **文件上传验证**: 所有上传的文件都经过格式和大小验证
2. **路径配置**: 使用配置文件管理，防止路径遍历
3. **配置验证**: 所有配置变更都经过验证
4. **默认主题保护**: 内置主题不可删除

## 性能优化

1. **缓存机制**: 配置加载时缓存到内存
2. **缩略图生成**: 背景图自动生成缩略图
3. **异步操作**: 所有API都使用异步方式
4. **增量更新**: 支持增量更新配置

## 扩展性

模块设计支持以下扩展：

1. **存储后端**: 可扩展支持云存储（S3、OSS等）
2. **更多格式**: 可添加新的图片/动画格式支持
3. **验证规则**: 可扩展配置验证规则
4. **主题引擎**: 可集成更多主题变量

## 版本历史

### v2.0 (2026-03-26)
- 初始版本发布
- 完整的LOGO/背景/动画/主题/布局管理
- 40+ RESTful API接口
- 完整的单元测试
- 详细的API文档

## 联系方式

如有问题或建议，请联系：
- 负责人: 康辅星 (162)
- 负责组: 辅弼星辰组
