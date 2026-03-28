#!/bin/bash
# 玄玑引擎前端四端 - 一键部署脚本（子域名版本）

set -e

echo "🚀 玄玑引擎前端四端 - 一键部署脚本"
echo "⏰ 开始时间: $(date)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 子域名规划${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "  官网: xuanji-ai.com (现有)"
echo "  用户端: app.xuanji-ai.com (新)"
echo "  配置端: config.xuanji-ai.com (新)"
echo "  开发者端: dev.xuanji-ai.com (新)"
echo "  管理端: admin.xuanji-ai.com (新)"
echo ""
echo -e "${YELLOW}⚠️  注意: 避免与现有官网端口冲突${NC}"
echo ""

# 步骤1: 本地打包
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📦 步骤 1: 本地打包四端${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

bash /workspace/projects/workspace/xuanji-engine-v2/scripts/build-locally.sh

# 步骤2: 配置服务器
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}⚙️  步骤 2: 配置OpenResty（子域名版本）${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}上传配置脚本到服务器...${NC}"
scp -i workspace/.secure/level4/ssh-keys/singapore.pem \
  /workspace/projects/workspace/xuanji-engine-v2/scripts/configure-server.sh \
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
    echo -e "${YELLOW}启动本地HTTP服务器 (端口 8888)...${NC}"
    bash /workspace/projects/workspace/xuanji-engine-v2/scripts/start-local-proxy.sh
else
    echo ""
    echo -e "${YELLOW}⚠️  跳过本地反向代理${NC}"
    echo ""
    echo "稍后可以手动启动:"
    echo "  bash scripts/start-local-proxy.sh"
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
echo "  官网: https://xuanji-ai.com"
echo "  用户端: https://app.xuanji-ai.com"
echo "  配置端: https://config.xuanji-ai.com"
echo "  开发者端: https://dev.xuanji-ai.com"
echo "  管理端: https://admin.xuanji-ai.com"
echo ""
echo -e "${BLUE}📂 文件位置:${NC}"
echo "  本地打包: /workspace/projects/workspace/xuanji-engine-v2/dist_packages/"
echo "  服务器目录: /var/www/xuanji-ai/"
echo "  备份目录: /usr/local/openresty/nginx/conf/backup-*"
echo ""
echo "⏰ 完成时间: $(date)"
