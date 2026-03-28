#!/bin/bash
# 一键部署脚本 - 玄玑引擎前端四端
# 用途：整合本地打包和服务器配置，一键完成部署

set -e

echo "🚀 玄玑引擎前端四端 - 一键部署脚本"
echo "⏰ 开始时间: $(date)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="/workspace/projects/workspace/xuanji-engine-v2/scripts"
PROJECT_ROOT="/workspace/projects/workspace/xuanji-engine-v2"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 部署流程${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "步骤 1: 本地打包四端"
echo "步骤 2: 配置本地反向代理"
echo "步骤 3: 上传配置到服务器"
echo "步骤 4: 在服务器上下载并部署"
echo ""

# 询问用户确认
read -p "是否继续？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "部署已取消"
    exit 0
fi

# 步骤1: 本地打包
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📦 步骤 1: 本地打包四端${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ -x "${SCRIPT_DIR}/build-locally.sh" ]; then
    bash "${SCRIPT_DIR}/build-locally.sh"
else
    echo -e "${RED}❌ 打包脚本不存在${NC}"
    exit 1
fi

# 步骤2: 配置服务器
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}⚙️  步骤 2: 配置OpenResty${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}上传配置脚本到服务器...${NC}"
scp -i workspace/.secure/level4/ssh-keys/singapore.pem \
    "${SCRIPT_DIR}/configure-server.sh" \
    root@43.160.237.122:/tmp/

echo -e "${YELLOW}在服务器上执行配置...${NC}"
ssh -i workspace/.secure/level4/ssh-keys/singapore.pem \
    root@43.160.237.122 "bash /tmp/configure-server.sh"

# 步骤3: 启动本地反向代理
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🌐 步骤 3: 启动本地反向代理${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

read -p "是否现在启动本地反向代理？(服务器需要从此下载) (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -x "${SCRIPT_DIR}/start-local-proxy.sh" ]; then
        bash "${SCRIPT_DIR}/start-local-proxy.sh"
    else
        echo -e "${RED}❌ 反向代理脚本不存在${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${YELLOW}⚠️  跳过本地反向代理${NC}"
    echo ""
    echo "稍后可以手动启动:"
    echo "  bash ${SCRIPT_DIR}/start-local-proxy.sh"
fi

# 完成
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🎉 部署流程完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}📋 下一步操作:${NC}"
echo ""
echo "在服务器上执行以下命令下载并部署:"
echo "  ssh -i workspace/.secure/level4/ssh-keys/singapore.pem root@43.160.237.122"
echo "  bash /tmp/download-from-local.sh"
echo ""
echo -e "${BLUE}🔗 访问地址:${NC}"
echo "  用户端: https://xuanji-ai.com"
echo "  配置端: https://config.xuanji-ai.com"
echo "  开发者端: https://dev.xuanji-ai.com"
echo "  管理端: https://admin.xuanji-ai.com"
echo ""
echo -e "${BLUE}📂 文件位置:${NC}"
echo "  本地打包: ${PROJECT_ROOT}/dist_packages/"
echo "  服务器目录: /var/www/xuanji-ai/"
echo "  备份目录: /usr/local/openresty/nginx/conf/backup-*"
echo ""
echo "⏰ 完成时间: $(date)"
