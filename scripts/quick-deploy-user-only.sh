#!/bin/bash
set -e

echo "🚨 快速部署脚本 - 仅部署user-client"
echo "⏰ 开始时间: $(date)"

SSH_KEY="/workspace/projects/workspace/.secure/level4/ssh-keys/singapore.pem"
SERVER="root@43.160.237.122"
PROJECT_DIR="/workspace/projects/workspace/xuanji-engine-v2"

echo ""
echo "========================================"
echo "📦 打包user-client"
echo "========================================"

cd $PROJECT_DIR/frontend/user-client/dist
tar -czf $PROJECT_DIR/dist_packages/app.tar.gz .

echo "✅ 打包完成"
echo ""
echo "========================================"
echo "🚀 部署到服务器"
echo "========================================"

# 创建远程目录
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "mkdir -p /var/www/xuanji-ai/app"

# 上传文件
echo "📤 上传app.tar.gz..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no $PROJECT_DIR/dist_packages/app.tar.gz $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "tar -xzf /tmp/app.tar.gz -C /var/www/xuanji-ai/app/ && rm /tmp/app.tar.gz"

# 设置权限
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "chown -R nginx:nginx /var/www/xuanji-ai/app && chmod -R 755 /var/www/xuanji-ai/app"

echo "✅ 部署完成"
echo ""
echo "========================================"
echo "🔧 配置OpenResty"
echo "========================================"

cat > /tmp/nginx-user-only.conf << 'NGINX_EOF'
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name app.xuanji-ai.com;
    return 301 https://app.xuanji-ai.com$request_uri;
}

# HTTPS server for app.xuanji-ai.com
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
NGINX_EOF

# 上传Nginx配置
scp -i $SSH_KEY -o StrictHostKeyChecking=no /tmp/nginx-user-only.conf $SERVER:/tmp/
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SERVER "mv /tmp/nginx-user-only.conf /usr/local/openresty/nginx/conf.d/ && openresty -s reload"

echo "✅ OpenResty配置完成"
echo ""
echo "========================================"
echo "🎉 部署完成"
echo "========================================"

echo ""
echo "📱 访问地址："
echo "https://app.xuanji-ai.com"
echo ""
echo "⏰ 完成时间: $(date)"
echo ""
echo "⚠️ 注意：只有user-client已部署"
echo "⚠️ 其他端（config、dev、admin、portal）需要修复后才能部署"
