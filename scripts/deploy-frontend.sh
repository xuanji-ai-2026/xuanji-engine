#!/bin/bash
# 玄玑引擎 - 前端部署脚本（打包+上传）
# 时间: 2026-03-26

set -e

PROJECT_DIR="/workspace/projects/workspace/xuanji-engine-v2"
DIST_DIR="$PROJECT_DIR/dist_packages"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SERVER="root@43.160.237.122"
SSH_KEY="/workspace/projects/workspace/.secure/level4/ssh-keys/singapore.pem"

echo "============================================"
echo "🚀 玄玑引擎前端部署"
echo "============================================"
echo "⏰ 开始时间: $(date)"
echo "📁 项目目录: $PROJECT_DIR"
echo "🌐 服务器: $SERVER"
echo ""

# 1. 打包前端（如果未打包）
echo "📦 步骤1: 检查打包产物"
echo "--------------------------------------------"

FRONTENDS=("user-client" "config-client" "developer-client" "admin-console")
for frontend in "${FRONTENDS[@]}"; do
    if [ ! -f "$PROJECT_DIR/frontend/$frontend/dist/index.html" ]; then
        echo "⚠️ $frontend 未打包，正在打包..."
        cd "$PROJECT_DIR/frontend/$frontend"
        npm run build
        echo "✅ $frontend 打包完成"
    else
        echo "✅ $frontend 已打包"
    fi
done

echo ""

# 2. 压缩打包产物
echo "📦 步骤2: 压缩打包产物"
echo "--------------------------------------------"

mkdir -p "$DIST_DIR"

for frontend in "${FRONTENDS[@]}"; do
    TAR_NAME="xuanji-$frontend-$TIMESTAMP.tar.gz"
    TAR_PATH="$DIST_DIR/$TAR_NAME"
    
    echo "   🗜️ 压缩 $frontend → $TAR_NAME"
    cd "$PROJECT_DIR/frontend/$frontend"
    tar -czf "$TAR_PATH" dist/
    
    SIZE=$(du -h "$TAR_PATH" | cut -f1)
    echo "   ✅ 压缩完成: $SIZE"
done

echo ""

# 3. 上传到服务器
echo "📤 步骤3: 上传到服务器"
echo "--------------------------------------------"

for frontend in "${FRONTENDS[@]}"; do
    TAR_NAME="xuanji-$frontend-$TIMESTAMP.tar.gz"
    TAR_PATH="$DIST_DIR/$TAR_NAME"
    
    echo "   📤 上传 $frontend..."
    scp -i "$SSH_KEY" "$TAR_PATH" "$SERVER:/tmp/"
    
    echo "   ✅ 上传完成"
done

echo ""

# 4. 在服务器上解压和部署
echo "🔧 步骤4: 在服务器上部署"
echo "--------------------------------------------"

SSH_CMD="ssh -i $SSH_KEY $SERVER"

# 创建部署脚本
DEPLOY_SCRIPT=$(cat <<'EOF'
#!/bin/bash
set -e

echo "🔧 开始部署到服务器..."

# 创建项目目录
mkdir -p /var/www/xuanji-ai

# 备份现有版本
for dir in user-client config-client developer-client admin-console; do
    if [ -d "/var/www/xuanji-ai/$dir" ]; then
        echo "   📦 备份 $dir..."
        mv "/var/www/xuanji-ai/$dir" "/var/www/xuanji-ai/$dir.backup.$(date +%Y%m%d_%H%M%S)"
    fi
done

# 解压新版本
for dir in user-client config-client developer-client admin-console; do
    TAR_FILE="/tmp/xuanji-$dir-"*.tar.gz
    echo "   📦 解压 $dir..."
    mkdir -p "/var/www/xuanji-ai/$dir"
    tar -xzf $TAR_FILE -C "/var/www/xuanji-ai/$dir" --strip-components=1
    echo "   ✅ $dir 解压完成"
done

# 设置权限
chown -R nobody:nobody /var/www/xuanji-ai
chmod -R 755 /var/www/xuanji-ai

echo ""
echo "✅ 部署完成！"
echo ""
echo "📁 部署目录: /var/www/xuanji-ai"
echo ""
echo "📋 目录结构:"
ls -la /var/www/xuanji-ai/
EOF
)

echo "$DEPLOY_SCRIPT" | $SSH_CMD "cat > /tmp/deploy-frontend.sh && chmod +x /tmp/deploy-frontend.sh"
$SSH_CMD "bash /tmp/deploy-frontend.sh"

echo ""

# 5. 验证部署
echo "✅ 步骤5: 验证部署"
echo "--------------------------------------------"

echo "检查服务器文件:"
$SSH_CMD "ls -la /var/www/xuanji-ai/*/index.html"

echo ""
echo "============================================"
echo "🎉 部署完成！"
echo "============================================"
echo "⏰ 完成时间: $(date)"
echo ""
echo "📁 本地打包: $DIST_DIR"
echo "🌐 服务器: $SERVER"
echo "📂 部署目录: /var/www/xuanji-ai"
echo ""
echo "🌐 访问地址:"
echo "   - 官网: https://xuanji-ai.com"
echo "   - 用户端: https://app.xuanji-ai.com"
echo "   - 配置端: https://config.xuanji-ai.com"
echo "   - 开发者端: https://dev.xuanji-ai.com"
echo "   - 管理端: https://admin.xuanji-ai.com"
echo ""
echo "⚠️ 下一步: 配置Nginx子域名路由"
echo "============================================"
