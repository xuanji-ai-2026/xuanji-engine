# 玄玑AI数字员工引擎

**版本**: v0.1.0 MVP  
**启动日期**: 2026-03-17  
**状态**: 🟢 开发中

---

## 项目结构

```
xuanji-engine/
├── src/
│   ├── ziwei/           # 紫微元灵 - 意图穿透
│   ├── lucen/           # 禄存星 - ReAct推理
│   ├── jumen/           # 巨门星 - 记忆系统
│   ├── lianzhen/        # 廉贞星 - 人格引擎
│   ├── wuqu/            # 武曲星 - 插件系统
│   ├── pojun/           # 破军星 - 执行层
│   ├── zuofu/           # 左辅星 - 底座
│   ├── youbi/           # 右弼星 - 安全
│   ├── tanlang/         # 贪狼星 - 交互
│   └── fubi/            # 辅弼星辰 - 开放平台
├── tests/               # 测试
├── docs/                # 文档
└── scripts/             # 脚本
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DeepSeek API Key
```

### 3. 启动服务

```bash
python -m uvicorn src.api.main:app --reload
```

## API文档

启动后访问: http://localhost:8000/docs

---

## 技术栈

- Python 3.11+
- FastAPI
- LangGraph
- DeepSeek API
- Redis (短期记忆)
- Milvus (长期记忆)
