#!/bin/bash
# 本地反向代理脚本 - 向服务器提供安装包
# 用途：在本地启动HTTP服务器，让服务器可以从本地获取打包文件

set -e

echo "🚀 启动本地反向代理 - 向服务器提供安装包"
echo "⏰ 开始时间: $(date)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
PACKAGES_DIR="/workspace/projects/workspace/xuanji-engine-v2/dist_packages"
SERVER_USER="root"
SERVER_HOST="43.160.237.122"
SERVER_KEY="workspace/.secure/level4/ssh-keys/singapore.pem"
SERVER_TEMP_DIR="/tmp/xuanji-deploy"
LOCAL_PORT=8888

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 反向代理配置${NC}"
echo -e "${BLUE}========================================${NC}"
echo "本地端口: ${LOCAL_PORT}"
echo "打包目录: ${PACKAGES_DIR}"
echo "服务器: ${SERVER_USER}@${SERVER_HOST}"
echo "服务器目录: ${SERVER_TEMP_DIR}"

# 检查打包文件
echo -e "${YELLOW}📂 检查打包文件...${NC}"
if [ ! -d "${PACKAGES_DIR}" ]; then
    echo -e "${RED}❌ 打包目录不存在${NC}"
    echo "请先运行: bash scripts/build-locally.sh"
    exit 1
fi

PACKAGE_COUNT=$(ls -1 "${PACKAGES_DIR}"/*.tar.gz 2>/dev/null | wc -l)
if [ "$PACKAGE_COUNT" -eq 0 ]; then
    echo -e "${RED}❌ 没有找到打包文件${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 找到 ${PACKAGE_COUNT} 个打包文件${NC}"

# 检查本地网络
echo -e "${YELLOW}🌐 检查本地网络...${NC}"
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "本地IP: ${LOCAL_IP}"

# 获取本地IP地址（用于服务器访问）
if [ -z "$LOCAL_IP" ]; then
    echo -e "${YELLOW}⚠️  无法获取本地IP，使用默认值${NC}"
    LOCAL_IP="10.0.0.1"  # 默认值，需要用户手动配置
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📤 上传部署脚本到服务器${NC}"
echo -e "${BLUE}========================================${NC}"

# 创建服务器端下载脚本
cat > /tmp/download-from-local.sh << EOF
#!/bin/bash
# 服务器端下载脚本
# 从本地反向代理下载安装包

set -e

LOCAL_IP="${LOCAL_IP}"
LOCAL_PORT="${LOCAL_PORT}"
TEMP_DIR="${SERVER_TEMP_DIR}"
APPS=("user-client" "config-client" "developer-client" "admin-console")

echo "📥 从本地反向代理下载安装包..."
echo "本地地址: http://\${LOCAL_IP}:\${LOCAL_PORT}"

# 创建目录
mkdir -p "\${TEMP_DIR}"/{user-client,config-client,developer-client,admin-console}

# 下载并解压
for app in "\${APPS[@]}"; do
    echo "📦 下载 \${app}..."
    
    case "\${app}" in
        user-client)
            PACKAGE="xuanji-user-client-v1.0.0.tar.gz"
            ;;
        config-client)
            PACKAGE="xuanji-config-client-v1.0.0.tar.gz"
            ;;
        developer-client)
            PACKAGE="xuanji-developer-client-v1.0.0.tar.gz"
            ;;
        admin-console)
            PACKAGE="xuanji-admin-console-v1.0.0.tar.gz"
            ;;
    esac
    
    # 下载
    if curl -f "http://\${LOCAL_IP}:\${LOCAL_PORT}/\${PACKAGE}" -o "\${TEMP_DIR}/\${PACKAGE}"; then
        echo "✅ \${app} 下载成功"
    else
        echo "❌ \${app} 下载失败"
        exit 1
    fi
    
    # 解压到临时目录
    echo "📂 解压 \${app}..."
    tar -xzf "\${TEMP_DIR}/\${PACKAGE}" -C "\${TEMP_DIR}/\${app}/"
    
    # 移动到正式目录
    echo "📦 部署 \${app}..."
    cp -r "\${TEMP_DIR}/\${app}/"/* /var/www/xuanji-ai/\${app}/
    
    # 设置权限
    chown -R nginx:nginx /var/www/xuanji-ai/\${app}
    chmod -R 755 /var/www/xuanji-ai/\${app}
    
    echo "✅ \${app} 部署完成"
done

echo ""
echo "🎉 所有应用部署完成！"
echo "重启OpenResty..."
/usr/local/openresty/nginx/sbin/nginx -s reload

echo ""
echo "✅ 部署成功！"
EOF

chmod +x /tmp/download-from-local.sh

# 上传脚本到服务器
echo -e "${YELLOW}📤 上传下载脚本到服务器...${NC}"
scp -i "${SERVER_KEY}" /tmp/download-from-local.sh ${SERVER_USER}@${SERVER_HOST}:/tmp/

echo -e "${GREEN}✅ 下载脚本已上传${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🌐 启动本地HTTP服务器${NC}"
echo -e "${BLUE}========================================${NC}"

# 使用Python启动HTTP服务器
echo -e "${YELLOW}🚀 启动HTTP服务器 (端口 ${LOCAL_PORT})...${NC}"
echo -e "${GREEN}本地服务器地址: http://${LOCAL_IP}:${LOCAL_PORT}${NC}"
echo ""
echo "📋 可以下载的文件:"
ls -lh "${PACKAGES_DIR}/*.tar.gz" 2>/dev/null || echo "  (无打包文件)"

echo ""
echo -e "${YELLOW}⏳ 服务器正在监听... (Ctrl+C 停止)${NC}"
echo ""

# 启动Python HTTP服务器
cd "${PACKAGES_DIR}"
python3 -m http.server ${LOCAL_PORT} &
HTTP_PID=$!

# 捕获Ctrl+C
trap 'echo ""; echo -e "${YELLOW}🛑 停止HTTP服务器...${NC}"; kill $HTTP_PID; exit 0' INT

# 等待HTTP服务器启动
sleep 2

# 检查HTTP服务器是否启动
if ps -p $HTTP_PID > /dev/null; then
    echo -e "${GREEN}✅ HTTP服务器已启动 (PID: ${HTTP_PID})${NC}"
else
    echo -e "${RED}❌ HTTP服务器启动失败${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 在服务器上执行以下命令下载并部署:${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "ssh -i ${SERVER_KEY} ${SERVER_USER}@${SERVER_HOST}"
echo "bash /tmp/download-from-local.sh"
echo ""

# 监控HTTP服务器
echo -e "${YELLOW}⏳ HTTP服务器运行中... (按 Ctrl+C 停止)${NC}"
echo -e "${YELLOW}📊 访问日志:${NC}"

tail -f /dev/null &
LOG_PID=$!

# 等待HTTP服务器
wait $HTTP_PID 2>/dev/null
kill $LOG_PID 2>/dev/null

echo ""
echo -e "${GREEN}👋 HTTP服务器已停止${NC}"
echo "⏰ 结束时间: $(date)"
