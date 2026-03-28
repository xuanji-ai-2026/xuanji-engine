# 玄玑引擎前端四端部署指南

**项目**: 玄玑引擎前端四端
**部署日期**: 2026-03-25
**服务器**: 腾讯云 43.160.237.122
**域名**: xuanji-ai.com

---

## 📋 部署前准备

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

# 检查Docker
docker --version

# 检查Nginx
nginx -v
```

### 2. 创建部署目录

```bash
# 在服务器上创建项目目录
mkdir -p /var/www/xuanji-ai

# 创建四个端的目录
cd /var/www/xuanji-ai
mkdir -p user-client config-client developer-client admin-console
```

---

## 🚀 部署步骤

### 第一步：构建前端应用（在本地）

#### 构建用户端
```bash
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/user-client

# 安装依赖
npm install

# 构建生产版本
npm run build

# 构建输出在 dist/ 目录
```

#### 构建配置端
```bash
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/config-client

# 安装依赖
npm install

# 构建生产版本
npm run build
```

#### 构建开发者端
```bash
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/developer-client

# 安装依赖
npm install

# 构建生产版本
npm run build
```

#### 构建管理端
```bash
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/admin-console

# 安装依赖
npm install

# 构建生产版本
npm run build
```

### 第二步：上传到服务器

```bash
# 上传用户端
scp -i workspace/.secure/level4/ssh-keys/singapore.pem -r \
  /workspace/projects/workspace/xuanji-engine-v2/frontend/user-client/dist/* \
  root@43.160.237.122:/var/www/xuanji-ai/user-client/

# 上传配置端
scp -i workspace/.secure/level4/ssh-keys/singapore.pem -r \
  /workspace/projects/workspace/xuanji-engine-v2/frontend/config-client/dist/* \
  root@43.160.237.122:/var/www/xuanji-ai/config-client/

# 上传开发者端
scp -i workspace/.secure/level4/ssh-keys/singapore.pem -r \
  /workspace/projects/workspace/xuanji-engine-v2/frontend/developer-client/dist/* \
  root@43.160.237.122:/var/www/xuanji-ai/developer-client/

# 上传管理端
scp -i workspace/.secure/level4/ssh-keys/singapore.pem -r \
  /workspace/projects/workspace/xuanji-engine-v2/frontend/admin-console/dist/* \
  root@43.160.237.122:/var/www/xuanji-ai/admin-console/
```

### 第三步：配置Nginx（在服务器上）

```bash
# 在服务器上创建Nginx配置
vi /etc/nginx/sites-available/xuanji-ai
```

**Nginx配置内容**：
```nginx
# 用户端（主站）
server {
    listen 80;
    server_name app.xuanji-ai.com;
    root /var/www/xuanji-ai/user-client;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API代理（可选，如果需要）
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 配置端
server {
    listen 80;
    server_name config.xuanji-ai.com;
    root /var/www/xuanji-ai/config-client;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# 开发者端
server {
    listen 80;
    server_name dev.xuanji-ai.com;
    root /var/www/xuanji-ai/developer-client;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# 管理端
server {
    listen 80;
    server_name admin.xuanji-ai.com;
    root /var/www/xuanji-ai/admin-console;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

#### 启用配置
```bash
# 创建软链接
ln -s /etc/nginx/sites-available/xuanji-ai /etc/nginx/sites-enabled/

# 测试Nginx配置
nginx -t

# 重启Nginx
systemctl restart nginx
```

### 第四步：配置SSL证书（可选，推荐）

```bash
# 安装Certbot
apt-get install certbot python3-certbot-nginx -y

# 获取SSL证书
certbot --nginx -d xuanji-ai.com -d config.xuanji-ai.com -d dev.xuanji-ai.com -d admin.xuanji-ai.com

# 自动续期
certbot renew --dry-run
```

### 第五步：配置域名DNS解析

在域名管理后台添加A记录：

| 子域名 | 记录类型 | 记录值 | TTL |
|--------|----------|--------|-----|
| @ | A | 43.160.237.122 | 600 |
| www | A | 43.160.237.122 | 600 |
| config | A | 43.160.237.122 | 600 |
| dev | A | 43.160.237.122 | 600 |
| admin | A | 43.160.237.122 | 600 |

---

## 📊 部署检查清单

### 环境检查
- [ ] Node.js >= 18.0
- [ ] npm >= 9.0
- [ ] Nginx已安装并运行
- [ ] 服务器端口80、443开放
- [ ] 防火墙已配置

### 文件检查
- [ ] 四个端都已构建
- [ ] dist/目录存在
- [ ] 文件已上传到服务器
- [ ] 权限配置正确

### 配置检查
- [ ] Nginx配置正确
- [ ] 域名DNS已解析
- [ ] SSL证书已配置（可选）
- [ ] API代理已配置（如需要）

---

## 🔧 常见问题

### 1. 构建失败

**问题**: `npm run build` 失败

**解决方案**:
```bash
# 清理缓存
rm -rf node_modules package-lock.json
npm cache clean --force

# 重新安装
npm install

# 重新构建
npm run build
```

### 2. Nginx 404错误

**问题**: 访问网站显示404

**解决方案**:
```bash
# 检查文件是否存在
ls -la /var/www/xuanji-ai/user-client/

# 检查Nginx配置
nginx -t

# 检查Nginx错误日志
tail -f /var/log/nginx/error.log
```

### 3. 刷新页面404（React Router问题）

**问题**: 页面刷新后404

**解决方案**: 确保Nginx配置中有 `try_files $uri $uri/ /index.html;`

### 4. API跨域问题

**问题**: 前端无法访问后端API

**解决方案**: 在Nginx中配置API代理，或在后端配置CORS

---

## 🚀 自动化部署脚本（可选）

### 创建一键部署脚本

```bash
#!/bin/bash
# deploy.sh

echo "🚀 开始部署玄玑引擎前端四端..."

# 1. 构建所有端
echo "📦 构建用户端..."
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/user-client
npm install && npm run build

echo "📦 构建配置端..."
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/config-client
npm install && npm run build

echo "📦 构建开发者端..."
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/developer-client
npm install && npm run build

echo "📦 构建管理端..."
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/admin-console
npm install && npm run build

# 2. 上传到服务器
echo "📤 上传到服务器..."
scp -i workspace/.secure/level4/ssh-keys/singapore.pem -r \
  /workspace/projects/workspace/xuanji-engine-v2/frontend/*/dist/* \
  root@43.160.237.122:/var/www/xuanji-ai/

# 3. 重启Nginx
echo "🔄 重启Nginx..."
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122 \
  "systemctl restart nginx"

echo "✅ 部署完成！"
echo "🌐 访问地址:"
echo "   用户端: https://xuanji-ai.com"
echo "   配置端: https://config.xuanji-ai.com"
echo "   开发者端: https://dev.xuanji-ai.com"
echo "   管理端: https://admin.xuanji-ai.com"
```

---

## 📞 技术支持

如果遇到问题，请联系：
- 技术负责人：张志远（002）
- 运维负责人：郑路由（112）

---

**祝部署顺利！** 🎉
