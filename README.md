# 玄玑引擎 (Xuanji Engine)

**版本**: v2.0  
**更新时间**: 2026-03-20

---

## 项目概述

玄玑引擎是一个基于LLM的AI数字员工引擎，采用十星模块架构设计。

## 版本历史

### v2.0 (当前版本)
- **状态**: 生产就绪
- **代码**: 293个Python文件，19,474+行代码
- **架构**: 十星模块架构
- **文档**: 包含v1.0和v2.0所有文档

### v1.0 (第一阶段)
- **状态**: 核心基础，保留参考
- **文档**: 见 `docs/v1_legacy/` 和 `docs/v1_phase1/`

## 目录结构

```
xuanji-engine-v2/
├── src/                    # 核心源代码
│   ├── ziwei/            # 意图识别模块
│   ├── lucen/            # ReAct引擎
│   ├── jumen/            # 记忆系统
│   ├── wuqu/             # 插件系统
│   ├── pohjun/           # 执行层
│   ├── zuofu/            # 底座层
│   ├── youbi/            # 安全层
│   ├── tanlang/          # 交互层
│   ├── fubi/             # 开放平台
│   └── lianzheng/        # 人格引擎
├── docs/                  # 文档
│   ├── v1_legacy/         # v1.0文档(参考)
│   ├── v1_phase1/         # 第一阶段文档
│   └── *.md              # v2.0文档
├── tests/                 # 测试文件
├── k8s/                  # K8s部署配置
└── config/               # 配置文件
```

## 快速开始

```bash
# 克隆项目
git clone git@github.com:xuanji-ai-2026/xuanji-engine.git
cd xuanji-engine-v2

# 安装依赖
pip3 install -r requirements.txt

# 运行
python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Docker部署

```bash
docker build -t xuanji-engine-v2 .
docker run -d -p 8000:8000 xuanji-engine-v2
```

## 更多信息

- [架构文档](docs/ARCHITECTURE.md)
- [API文档](docs/API.md)
- [部署指南](docs/DEPLOYMENT.md)
- [用户指南](docs/USER_GUIDE.md)

## 许可证

MIT
