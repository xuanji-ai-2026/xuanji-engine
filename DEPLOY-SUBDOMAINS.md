# 玄玑引擎前端四端部署指南 - 子域名版本

**方案**: 本地打包 + 服务器反向代理  
**优势**: 避免积分消耗 + 避免端口冲突 + 子域名部署

---

## 🎯 子域名规划

| 子域名 | 用途 | 目录 | 说明 |
|--------|------|------|------|
| xuanji-ai.com | 官方门户网站 | official-portal | 原有官网，保持不变 |
| app.xuanji-ai.com | 用户端 | user-client | 用户应用入口 |
| config.xuanji-ai.com | 配置端 | config-client | 配置管理后台 |
| dev.xuanji-ai.com | 开发者端 | developer-client | 开发者平台 |
| admin.xuanji-ai.com | 管理端 | admin-console | 系统管理 |

---

## 📋 部署前检查

### 1. 服务器环境检查

#### 连接到服务器
```bash
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122
```

#### 检查环境
```bash
# 检查Node.js版本（需要>=18.0）
node --version

# 检查npm版本（需要>=9.0）
npm --version

# 检查OpenResty
/usr/local/openresty/nginx/sbin/nginx -v

# 检查Nginx
nginx -v
```

### 2. 创建部署目录

```bash
# 在服务器上创建项目目录
mkdir -p /var/www/xuanji-ai

# 创建四个端的目录
cd /var/www/xuanji-ai
mkdir -p user-client config-client developer-client admin-console official-portal
```

---

## 🚀 部署步骤

### 第一步：本地打包四端

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/build-locally.sh
```

**输出**:
- `dist_packages/xuanji-user-client-v1.0.0.tar.gz`
- `dist_packages/xuanji-config-client-v1.0.0.tar.gz`
- `dist_packages/xuanji-developer-client-v1.0.0.tar.gz`
- `dist_packages/xuanji-admin-console-v1.0.0.tar.gz`

### 第二步：配置OpenResty

```bash
# 上传配置脚本
scp -i workspace/.secure/level4/ssh-keys/singapore.pem \
  scripts/configure-server.sh \
  root@43.160.237.122:/tmp/

# 执行配置
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem \
  root@43.160.237.122 "bash /tmp/configure-server.sh"
```

### 第三步：启动本地反向代理

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/start-local-proxy.sh
```

### 第四步：服务器下载并部署

```bash
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122
bash /tmp/download-from-local.sh
```

---

## 🔧 OpenResty配置要点

### 子域名配置

```nginx
# HTTP重定向到HTTPS
server {
    listen 80;
    server_name app.xuanji-ai.com config.xuanji-ai.com dev.xuanji-ai.com admin.xuanji-ai.com;
    
    return 301 https://$server_name$request_uri;
}

# 官网（已存在）
server {
    listen 443 ssl http2;
    server_name xuanji-ai.com;
    root /var/www/xuanji-ai/official-portal;
}

# 用户端
server {
    listen 443 ssl http2;
    server_name app.xuanji-ai.com;
    root /var/www/xuanji-ai/user-client;
}

# 其他子域名...
```

### API代理

所有子域名都支持API代理到后端：
```nginx
location /api/ {
    proxy_pass http://localhost:5000;
    # ... 其他配置
}
```

---

## ✅ 部署验证

### 1. 检查文件
```bash
ls -la /var/www/xuanji-ai/{user-client,config-client,developer-client,admin-console}
```

### 2. 访问测试
```bash
curl -I https://xuanji-ai.com
curl -I https://app.xuanji-ai.com
curl -I https://config.xuanji-ai.com
curl -I https://dev.xuanji-ai.com
curl -I https://admin.xuanji-ai.com
```

---

## 🔄 快速部署

### 一键部署

```bash
cd /workspace/projects/workspace/xuanji-engine-v2
bash scripts/deploy-oneclick.sh
```

然后在服务器上：
```bash
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122
bash /tmp/download-from-local.sh
```

---

## 🎯 访问地址

| 子域名 | 用途 | 地址 |
|--------|------|------|
| xuanji-ai.com | 官网 | https://xuanji-ai.com |
| app.xuanji-ai.com | 用户端 | https://app.xuanji-ai.com |
| config.xuanji-ai.com | 配置端 | https://config.xuanji-ai.com |
| dev.xuanji-ai.com | 开发者端 | https://dev.xuanji-ai.com |
| admin.xuanji-ai.com | 管理端 | https://admin.xuanji-ai.com |

---

## ⚠️ 注意事项

1. **子域名DNS配置**
   - 在域名管理后台添加5个A记录
   - 全部指向 43.160.237.122

2. **SSL证书**
   - 已配置通配符证书
   - 支持所有子域名

3. **端口冲突**
   - 80/443端口已配置，不会有冲突
   - 使用子域名区分不同应用

4. **回滚**
   - 配置已自动备份
   - 回滚脚本: `/tmp/rollback-xuanji.sh`

---

**祝部署顺利！** 🎉
