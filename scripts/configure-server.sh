#!/bin/bash
# 服务器端配置脚本 - 玄玑引擎前端四端
# 用途：在服务器上配置OpenResty，设置子域名反向代理

set -e

echo "🚀 配置玄玑引擎前端四端 - 服务器端"
echo "⏰ 开始时间: $(date)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置变量
BASE_DIR="/var/www/xuanji-ai"
BACKEND_API="http://localhost:5000"  # 后端API地址
OPENRESTY_CONF_DIR="/usr/local/openresty/nginx/conf"
TEMP_DIR="/tmp/xuanji-deploy"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 配置信息${NC}"
echo -e "${BLUE}========================================${NC}"
echo "项目目录: ${BASE_DIR}"
echo "后端API: ${BACKEND_API}"
echo "OpenResty配置: ${OPENRESTY_CONF_DIR}"
echo "用户端域名: app.xuanji-ai.com (官网为 xuanji-ai.com)"

# 创建目录
echo -e "${YELLOW}📁 创建目录结构...${NC}"
mkdir -p "${BASE_DIR}"/{user-client,config-client,developer-client,admin-console}
mkdir -p "${TEMP_DIR}"

# 检查现有端口占用
echo -e "${YELLOW}🔍 检查端口占用...${NC}"
if netstat -tuln | grep -q ':80 '; then
    echo -e "${YELLOW}⚠️  端口80已被占用（可能官网）${NC}"
fi
if netstat -tuln | grep -q ':443 '; then
    echo -e "${YELLOW}⚠️  端口443已被占用（可能官网）${NC}"
fi

# 备份现有配置
echo -e "${YELLOW}💾 备份现有OpenResty配置...${NC}"
BACKUP_DIR="/usr/local/openresty/nginx/conf/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "${BACKUP_DIR}"
cp -r ${OPENRESTY_CONF_DIR}/*.conf "${BACKUP_DIR}/" 2>/dev/null || true
echo -e "${GREEN}✅ 配置已备份到: ${BACKUP_DIR}${NC}"

# 创建OpenResty配置
echo -e "${YELLOW}⚙️  创建OpenResty配置...${NC}"

cat > "${OPENRESTY_CONF_DIR}/xuanji-ai.conf" << 'EOF'
# 玄玑引擎前端四端 - OpenResty配置
# 子域名部署方案

# 全局配置
upstream backend_api {
    server localhost:5000 max_fails=3 fail_timeout=30s;
}

# 缓存配置
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=xuanji_cache:10m max_size=1g inactive=60m use_temp_path=off;

# HTTP 服务器（重定向到HTTPS）
server {
    listen 80;
    server_name app.xuanji-ai.com config.xuanji-ai.com dev.xuanji-ai.com admin.xuanji-ai.com;
    
    # Let's Encrypt验证
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # 重定向到HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS 服务器 - 官网
server {
    listen 443 ssl http2;
    server_name app.xuanji-ai.com;
    
    root /var/www/xuanji-ai/official-portal;  # 官网目录
    index index.html;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    
    # 其他配置...
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# HTTPS 服务器 - 用户端
server {
    listen 443 ssl http2;
    server_name app.xuanji-ai.com;
    
    # SSL证书配置
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;
    
    # 静态文件
    root /var/www/xuanji-ai/user-client;
    index index.html;
    
    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # SPA路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API代理
    location /api/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # WebSocket支持
    location /ws/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# HTTPS 服务器 - 配置端
server {
    listen 443 ssl http2;
    server_name config.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    root /var/www/xuanji-ai/config-client;
    index index.html;
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTPS 服务器 - 开发者端
server {
    listen 443 ssl http2;
    server_name dev.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    root /var/www/xuanji-ai/developer-client;
    index index.html;
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTPS 服务器 - 管理端
server {
    listen 443 ssl http2;
    server_name admin.xuanji-ai.com;
    
    ssl_certificate /etc/letsencrypt/live/xuanji-ai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xuanji-ai.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # IP白名单（可选）
    # allow 1.2.3.4;
    # deny all;
    
    root /var/www/xuanji-ai/admin-console;
    index index.html;
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 创建临时目录供本地反向代理
echo -e "${YELLOW}📂 创建临时目录供本地反向代理...${NC}"
mkdir -p "${TEMP_DIR}"/{user-client,config-client,developer-client,admin-console}

# 设置权限
echo -e "${YELLOW}🔒 设置文件权限...${NC}"
chown -R nginx:nginx "${BASE_DIR}"
chown -R nginx:nginx "${TEMP_DIR}"
chmod -R 755 "${BASE_DIR}"
chmod -R 755 "${TEMP_DIR}"

# 测试配置
echo -e "${YELLOW}🧪 测试OpenResty配置...${NC}"
if /usr/local/openresty/nginx/sbin/nginx -t 2>&1 | grep -q "syntax is ok"; then
    echo -e "${GREEN}✅ 配置测试通过${NC}"
else
    echo -e "${RED}❌ 配置测试失败${NC}"
    echo "请检查配置文件"
    exit 1
fi

# 创建回滚脚本
echo -e "${YELLOW}💾 创建回滚脚本...${NC}"
cat > /tmp/rollback-xuanji.sh << 'EOF'
#!/bin/bash
# 回滚脚本
BACKUP_DIR="/usr/local/openresty/nginx/conf/backup-latest"
cp -r ${BACKUP_DIR}/*.conf /usr/local/openresty/nginx/conf/
/usr/local/openresty/nginx/sbin/nginx -s reload
echo "已回滚到备份配置"
EOF
chmod +x /tmp/rollback-xuanji.sh

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ 服务器配置完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📋 配置摘要:${NC}"
echo "  - 子域名已配置"
echo "  - HTTP自动重定向到HTTPS"
echo "  - OpenResty配置已创建"
echo "  - 备份已保存"
echo ""
echo -e "${BLUE}📂 目录结构:${NC}"
echo "  ${BASE_DIR}/"
echo "    ├── user-client/"
echo "    ├── config-client/"
echo "    ├── developer-client/"
echo "    └── admin-console/"
echo ""
echo -e "${BLUE}📁 临时目录（供本地反向代理）:${NC}"
echo "  ${TEMP_DIR}/"
echo ""
echo -e "${BLUE}🔗 访问地址:${NC}"
echo "  官网: https://xuanji-ai.com"
echo "  用户端: https://app.xuanji-ai.com"
echo "  配置端: https://config.xuanji-ai.com"
echo "  开发者端: https://dev.xuanji-ai.com"
echo "  管理端: https://admin.xuanji-ai.com"
echo ""
echo -e "${BLUE}下一步:${NC}"
echo "  1. 本地运行打包脚本"
echo "  2. 上传打包文件到服务器"
echo "  3. 解压到对应目录"
echo "  4. 重启OpenResty"
echo ""
echo -e "${YELLOW}⚠️  注意事项:${NC}"
echo "  - 备份目录: ${BACKUP_DIR}"
echo "  - 回滚脚本: /tmp/rollback-xuanji.sh"
echo "  - 已有官网端口检查: 80/443"
echo ""
echo "⏰ 完成时间: $(date)"
