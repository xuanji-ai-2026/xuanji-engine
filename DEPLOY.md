# 玄玑引擎前端四端部署指南

**方案**: 本地打包 + 服务器反向代理  
**优势**: 避免积分消耗、避免端口冲突、使用子域名

---

## 🎯 部署方案概述

### 架构
```
本地开发机
├── 1. 本地打包四端 (build-locally.sh)
│   └── 生成: dist_packages/*.tar.gz
├── 2. 启动HTTP服务器 (start-local-proxy.sh)
│   └── 端口: 8888
└── 3. 服务器通过HTTP下载
    ↓
腾讯云服务器 (43.160.237.122)
├── OpenResty配置 (configure-server.sh)
│   └── 子域名反向代理
├── 下载并解压
└── 重启OpenResty
```

### 子域名规划

| 子域名 | 用途 | 目录 |
|--------|------|------|
| xuanji-ai.com | 官方门户网站 | official-portal |
| app.xuanji-ai.com | 用户端 | user-client |
| config.xuanji-ai.com | 配置端 | config-client |
| dev.xuanji-ai.com | 开发者端 | developer-client |
| admin.xuanji-ai.com | 管理端 | admin-console |

### 端口规划

| 端口 | 用途 | 说明 |
|------|------|------|
| 80 | HTTP | 已有官网使用，自动重定向到HTTPS |
| 443 | HTTPS | 已配置SSL证书，OpenResty监听 |
| 5000 | 后端API | 后端服务端口 |
| 8888 | 本地HTTP | 本地反向代理端口（临时） |

---

## 🚀 快速部署

### 方式一：一键部署（推荐）

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/deploy-oneclick.sh
```

**执行流程**:
1. ✅ 本地打包四端
2. ✅ 配置OpenResty（上传配置脚本到服务器）
3. ✅ 启动本地反向代理（供服务器下载）
4. ✅ 提示在服务器上执行下载命令

### 方式二：分步部署

#### 步骤1: 本地打包

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/build-locally.sh
```

**输出**:
- `dist_packages/xuanji-user-client-v1.0.0.tar.gz`
- `dist_packages/xuanji-config-client-v1.0.0.tar.gz`
- `dist_packages/xuanji-developer-client-v1.0.0.tar.gz`
- `dist_packages/xuanji-admin-console-v1.0.0.tar.gz`
- `dist_packages/VERSION.md`
- `dist_packages/SHA256SUMS.txt`

#### 步骤2: 配置服务器

```bash
# 上传配置脚本
scp -i workspace/.secure/level4/ssh-keys/singapore.pem \
  scripts/configure-server.sh \
  root@43.160.237.122:/tmp/

# 执行配置
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem \
  root@43.160.237.122 "bash /tmp/configure-server.sh"
```

**配置内容**:
- 创建子域名目录
- 配置OpenResty
- 备份现有配置
- 创建回滚脚本

#### 步骤3: 启动本地反向代理

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/start-local-proxy.sh
```

**功能**:
- 在本地启动HTTP服务器（端口8888）
- 让服务器可以从本地下载打包文件
- 提供下载命令提示

#### 步骤4: 服务器下载并部署

**在服务器上执行**:

```bash
# 连接服务器
ssh -i ~/.ssh/singapore.pem root@43.160.237.122

# 执行下载脚本
bash /tmp/download-from-local.sh
```

**下载脚本会**:
1. 从本地反向代理下载四个tar.gz文件
2. 解压到临时目录
3. 复制到正式目录
4. 设置权限
5. 重启OpenResty

---

## 📋 脚本说明

### build-locally.sh
**功能**: 本地打包四端  
**输出**: `dist_packages/*.tar.gz`  
**优点**: 零积分消耗

### start-local-proxy.sh
**功能**: 启动本地HTTP服务器，供服务器下载  
**端口**: 8888  
**优点**: 服务器可以从本地获取安装包

### configure-server.sh
**功能**: 配置OpenResty、创建目录、设置权限  
**位置**: 服务器端执行  
**优点**: 避免端口冲突、子域名配置

### deploy-oneclick.sh
**功能**: 一键执行上述所有步骤  
**使用**: 推荐使用此脚本

---

## 🔧 OpenResty配置特点

### 1. 子域名支持
- ✅ 官网: `xuanji-ai.com`
- ✅ 用户端: `app.xuanji-ai.com`
- ✅ 配置端: `config.xuanji-ai.com`
- ✅ 开发者端: `dev.xuanji-ai.com`
- ✅ 管理端: `admin.xuanji-ai.com`

### 2. HTTP重定向
- ✅ HTTP自动重定向到HTTPS
- ✅ Let's Encrypt验证支持

### 3. Gzip压缩
- ✅ 静态资源压缩
- ✅ 减少带宽消耗

### 4. 缓存配置
- ✅ 静态资源缓存30天
- ✅ API代理绕过缓存

### 5. API代理
- ✅ 所有子域名支持API代理
- ✅ WebSocket支持
- ✅ 跨域处理

---

## ✅ 部署验证

### 1. 检查文件
```bash
# 在服务器上检查
ls -la /var/www/xuanji-ai/{user-client,config-client,developer-client,admin-console}
```

### 2. 检查Nginx配置
```bash
# 在服务器上检查
/usr/local/openresty/nginx/sbin/nginx -t
```

### 3. 检查SSL证书
```bash
# 在服务器上检查
ls -la /etc/letsencrypt/live/xuanji-ai.com/
```

### 4. 访问测试
```bash
# 访问测试
curl -I https://xuanji-ai.com
curl -I https://app.xuanji-ai.com
curl -I https://config.xuanji-ai.com
curl -I https://dev.xuanji-ai.com
curl -I https://admin.xuanji-ai.com
```

---

## 🔄 回滚方案

如果部署出现问题，可以快速回滚：

```bash
# 在服务器上执行
bash /tmp/rollback-xuanji.sh
```

**回滚脚本会**:
1. 从备份目录恢复配置
2. 重启OpenResty

---

## 📊 避免积分消耗

### 传统的服务器部署
```
❌ 在服务器上执行 npm install
❌ 在服务器上执行 npm run build
❌ 消耗大量积分（LLM调用）
```

### 本地打包方案
```
✅ 本地打包（零积分消耗）
✅ 只上传最终的tar.gz文件
✅ 服务器只需解压和配置
✅ 避免在服务器上运行构建命令
```

---

## 🎯 下一步

1. **运行一键部署脚本**
   ```bash
   bash scripts/deploy-oneclick.sh
   ```

2. **在服务器上执行下载**
   ```bash
   ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122
   bash /tmp/download-from-local.sh
   ```

3. **访问测试**
   - 官网: https://xuanji-ai.com
   - 用户端: https://app.xuanji-ai.com
   - 配置端: https://config.xuanji-ai.com
   - 开发者端: https://dev.xuanji-ai.com
   - 管理端: https://admin.xuanji-ai.com

---

**祝部署顺利！** 🎉
