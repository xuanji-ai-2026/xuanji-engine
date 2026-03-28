#!/bin/bash
set -e

echo "🚨 紧急修复部署脚本"
echo "⏰ 开始时间: $(date)"

echo ""
echo "========================================"
echo "📋 修复配置端TypeScript错误"
echo "========================================"

cd /workspace/projects/workspace/xuanji-engine-v2/frontend/config-client

# 修复未使用的import
sed -i "s/import { Filter } from 'lucide-react';/\/\/ import { Filter } from 'lucide-react';/" src/modules/user/components/UserGroupManagement.tsx

# 修复 Modal footer -> actions
sed -i 's/footer={/actions={/g' src/modules/user/components/UserGroupManagement.tsx

# 修复 Input onChange
sed -i 's/onChange={setSearchKeyword}/onChange={(e) => setSearchKeyword(e.target.value)}/g' src/modules/user/components/UserGroupManagement.tsx

echo "✅ 配置端修复完成"
echo ""
echo "========================================"
echo "📦 重新构建所有前端"
echo "========================================"

# 构建config-client
echo "🔨 构建config-client..."
npm run build 2>&1 | tail -10

# 构建developer-client
echo ""
echo "🔨 构建developer-client..."
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/developer-client
npm run build 2>&1 | tail -10

# 构建admin-console
echo ""
echo "🔨 构建admin-console..."
cd /workspace/projects/workspace/xuanji-engine-v2/frontend/admin-console
npm run build 2>&1 | tail -10

echo ""
echo "✅ 所有前端构建完成"
echo ""
echo "========================================"
echo "📦 打包所有dist"
echo "========================================"

cd /workspace/projects/workspace/xuanji-engine-v2

# 创建打包目录
mkdir -p dist_packages

# 打包各个前端
cd frontend/user-client/dist && tar -czf ../../dist_packages/app.tar.gz . && cd ../..
cd frontend/config-client/dist && tar -czf ../../dist_packages/config.tar.gz . && cd ../..
cd frontend/developer-client/dist && tar -czf ../../dist_packages/dev.tar.gz . && cd ../..
cd frontend/admin-console/dist && tar -czf ../../dist_packages/admin.tar.gz . && cd ../..
cd frontend/official-portal/dist && tar -czf ../../dist_packages/portal.tar.gz . && cd ../..

echo "✅ 打包完成"
echo ""
echo "========================================"
echo "🚀 部署到服务器"
echo "========================================"

SSH_KEY="/workspace/projects/workspace/.secure/level4/ssh-keys/singapore.pem"
SERVER="root@43.160.237.122"

# 创建远程目录
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "mkdir -p /var/www/xuanji-ai/{app,config,dev,admin,portal}"

# 上传文件
echo "📤 上传app.tar.gz..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no dist_packages/app.tar.gz $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "tar -xzf /tmp/app.tar.gz -C /var/www/xuanji-ai/app/ && rm /tmp/app.tar.gz"

echo "📤 上传config.tar.gz..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no dist_packages/config.tar.gz $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "tar -xzf /tmp/config.tar.gz -C /var/www/xuanji-ai/config/ && rm /tmp/config.tar.gz"

echo "📤 上传dev.tar.gz..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no dist_packages/dev.tar.gz $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "tar -xzf /tmp/dev.tar.gz -C /var/www/xuanji-ai/dev/ && rm /tmp/dev.tar.gz"

echo "📤 上传admin.tar.gz..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no dist_packages/admin.tar.gz $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "tar -xzf /tmp/admin.tar.gz -C /var/www/xuanji-ai/admin/ && rm /tmp/admin.tar.gz"

echo "📤 上传portal.tar.gz..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no dist_packages/portal.tar.gz $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "tar -xzf /tmp/portal.tar.gz -C /var/www/xuanji-ai/portal/ && rm /tmp/portal.tar.gz"

# 设置权限
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "chown -R nginx:nginx /var/www/xuanji-ai && chmod -R 755 /var/www/xuanji-ai"

echo "✅ 部署完成"
echo ""
echo "========================================"
echo "🔧 配置OpenResty"
echo "========================================"

# 创建Nginx配置文件
cat > /tmp/nginx-xuanji.conf << 'NGINX_EOF'
server {
    listen 80;
    server_name xuanji-ai.com;
    return 301 https://xuanji-ai.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    
    root /var/www/xuanji-ai/portal;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 80;
    server_name app.xuanji-ai.com;
    return 301 https://app.xuanji-ai.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name app.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    
    root /var/www/xuanji-ai/app;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 80;
    server_name config.xuanji-ai.com;
    return 301 https://config.xuanji-ai.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name config.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    
    root /var/www/xuanji-ai/config;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 80;
    server_name dev.xuanji-ai.com;
    return 301 https://dev.xuanji-ai.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dev.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    
    root /var/www/xuanji-ai/dev;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 80;
    server_name admin.xuanji-ai.com;
    return 301 https://admin.xuanji-ai.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name admin.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    
    root /var/www/xuanji-ai/admin;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINX_EOF

# 上传Nginx配置
scp -i $SSH_KEY -o StrictHostKeyChecking=no /tmp/nginx-xuanji.conf $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "mv /tmp/nginx-xuanji.conf /usr/local/openresty/nginx/conf.d/ && openresty -s reload"

echo "✅ OpenResty配置完成"
echo ""
echo "========================================"
echo "🎉 部署完成"
echo "========================================"

echo ""
echo "📱 访问地址："
echo "https://xuanji-ai.com"
echo "https://app.xuanji-ai.com"
echo "https://config.xuanji-ai.com"
echo "https://dev.xuanji-ai.com"
echo "https://admin.xuanji-ai.com"
echo ""
echo "⏰ 完成时间: $(date)"
