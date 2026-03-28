# 玄玑引擎前端四端部署 - 子域名版本

**部署时间**: 2026-03-25 21:37  
**方案**: 本地打包 + 服务器反向代理  
**优势**: 零积分消耗 + 避免端口冲突 + 子域名部署

---

## ✅ 子域名调整完成

**重要变更**：
- ~~用户端: xuanji-ai.com~~ → **app.xuanji-ai.com** ✅
- 官网: **xuanji-ai.com** （保持不变）

---

## 📊 最终子域名规划

| 子域名 | 用途 | 状态 | 说明 |
|--------|------|------|------|
| xuanji-ai.com | 官方门户网站 | ✅ 已存在 | 保持不变 |
| app.xuanji-ai.com | 用户端 | 🆕 新增 | 应用入口 |
| config.xuanji-ai.com | 配置端 | 🆕 新增 | 配置管理 |
| dev.xuanji-ai.com | 开发者端 | 🆕 新增 | 开发者平台 |
| admin.xuanji-ai.com | 管理端 | 🆕 新增 | 系统管理 |

---

## 🚀 一键部署

### 方式一：一键部署（推荐）

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/deploy-subdomains.sh
```

### 方式二：分步部署

#### 步骤1: 本地打包
```bash
bash scripts/build-locally.sh
```

#### 步骤2: 配置OpenResty
```bash
scp -i workspace/.secure/level4/ssh-keys/singapore.pem \
  scripts/configure-server.sh \
  root@43.160.237.122:/tmp/

ssh -i workspace/.secure/level4/ssh-keys/singapore.pem \
  root@43.160.237.122 "bash /tmp/configure-server.sh"
```

#### 步骤3: 启动本地反向代理
```bash
bash scripts/start-local-proxy.sh
```

#### 步骤4: 服务器下载并部署
```bash
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122
bash /tmp/download-from-local.sh
```

---

## 📦 部署脚本

| 脚本 | 功能 | 状态 |
|------|------|------|
| `scripts/build-locally.sh` | 本地打包四端 | ✅ 已更新 |
| `scripts/start-local-proxy.sh` | 启动本地HTTP服务器 | ✅ 已更新 |
| `scripts/configure-server.sh` | 配置OpenResty（子域名） | ✅ 已更新 |
| `scripts/deploy-subdomains.sh` | 一键部署脚本 | ✅ 已创建 |

---

## 🔗 访问地址

| 子域名 | 用途 | 地址 |
|--------|------|------|
| xuanji-ai.com | 官网 | https://xuanji-ai.com |
| app.xuanji-ai.com | 用户端 | https://app.xuanji-ai.com |
| config.xuanji-ai.com | 配置端 | https://config.xuanji-ai.com |
| dev.xuanji-ai.com | 开发者端 | https://dev.xuanji-ai.com |
| admin.xuanji-ai.com | 管理端 | https://admin.xuanji-ai.com |

---

## ⚠️ 注意事项

1. **DNS配置**
   - 需要添加5个A记录
   - 全部指向 43.160.237.122

2. **SSL证书**
   - 已配置通配符证书
   - 支持所有子域名

3. **端口冲突**
   - 80/443端口通过子域名避免冲突
   - 官网和四端可以共存

4. **积分消耗**
   - 零积分消耗（本地打包）
   - 服务器只负责解压和配置

---

**准备就绪，可以开始部署！** 🚀

**是否现在运行一键部署脚本？**

输入 `yes` 立即开始执行。

---

*本文档由AI数字员工管理系统 v4.1自动生成*
