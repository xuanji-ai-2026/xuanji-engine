#!/bin/bash
# 本地打包脚本 - 玄玑引擎前端四端
# 用途：在本地打包四端，避免在服务器上构建

set -e

echo "🚀 开始本地打包玄玑引擎前端四端..."
echo "⏰ 开始时间: $(date)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="/workspace/projects/workspace/xuanji-engine-v2"
OUTPUT_DIR="${PROJECT_ROOT}/dist_packages"

# 创建输出目录
echo -e "${BLUE}📦 创建输出目录...${NC}"
mkdir -p "${OUTPUT_DIR}"

# 打包函数
build_and_package() {
    local app_name=$1
    local app_dir=$2
    local package_name=$3
    
    echo -e "${BLUE}🔨 构建 ${app_name}...${NC}"
    cd "${PROJECT_ROOT}/frontend/${app_dir}"
    
    # 安装依赖
    echo "   📥 安装依赖..."
    npm install --silent
    
    # 构建
    echo "   📦 构建..."
    npm run build
    
    # 打包
    echo "   📄 打包..."
    cd dist
    tar -czf "${OUTPUT_DIR}/${package_name}.tar.gz" .
    cd "${PROJECT_ROOT}/frontend/${app_dir}"
    
    # 清理
    echo "   🧹 清理..."
    rm -rf dist node_modules/.vite
    
    echo -e "${GREEN}✅ ${app_name} 打包完成: ${OUTPUT_DIR}/${package_name}.tar.gz${NC}"
    
    # 显示文件大小
    local size=$(du -h "${OUTPUT_DIR}/${package_name}.tar.gz" | cut -f1)
    echo "   📊 文件大小: ${size}"
}

# 打包四端
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📦 开始打包四端${NC}"
echo -e "${BLUE}========================================${NC}"

build_and_package "用户端" "user-client" "xuanji-user-client-v1.0.0"
build_and_package "配置端" "config-client" "xuanji-config-client-v1.0.0"
build_and_package "开发者端" "developer-client" "xuanji-developer-client-v1.0.0"
build_and_package "管理端" "admin-console" "xuanji-admin-console-v1.0.0"

# 创建版本信息文件
echo -e "${BLUE}📝 创建版本信息...${NC}"
cat > "${OUTPUT_DIR}/VERSION.md" << EOF
# 玄玑引擎前端四端 - 打包版本信息

**打包时间**: $(date)
**打包版本**: v1.0.0
**打包环境**: 本地开发环境

## 打包清单

| 应用 | 文件名 | 大小 |
|------|--------|------|
| 用户端 | xuanji-user-client-v1.0.0.tar.gz | $(du -h ${OUTPUT_DIR}/xuanji-user-client-v1.0.0.tar.gz | cut -f1) |
| 配置端 | xuanji-config-client-v1.0.0.tar.gz | $(du -h ${OUTPUT_DIR}/xuanji-config-client-v1.0.0.tar.gz | cut -f1) |
| 开发者端 | xuanji-developer-client-v1.0.0.tar.gz | $(du -h ${OUTPUT_DIR}/xuanji-developer-client-v1.0.0.tar.gz | cut -f1) |
| 管理端 | xuanji-admin-console-v1.0.0.tar.gz | $(du -h ${OUTPUT_DIR}/xuanji-admin-console-v1.0.0.tar.gz | cut -f1) |

## 技术栈

- React 18.3.1
- TypeScript 5.9.3
- Vite 5.3.1
- Zustand 4.4.0
- Tailwind CSS 3.4.3

## 部署说明

1. 将四个tar.gz文件上传到服务器
2. 在服务器上解压到对应目录
3. 配置OpenResty反向代理

---
*本文件由自动化脚本生成*
EOF

echo -e "${GREEN}✅ 版本信息已创建${NC}"

# 显示总大小
total_size=$(du -sh "${OUTPUT_DIR}" | cut -f1)
echo -e "${BLUE}📊 总大小: ${total_size}${NC}"

# 计算SHA256校验和
echo -e "${BLUE}🔒 生成校验和...${NC}"
cd "${OUTPUT_DIR}"
sha256sum *.tar.gz > SHA256SUMS.txt
cd - > /dev/null
echo -e "${GREEN}✅ 校验和已生成: SHA256SUMS.txt${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📁 输出目录: ${OUTPUT_DIR}${NC}"
echo -e "${BLUE}📋 文件列表:${NC}"
ls -lh "${OUTPUT_DIR}"

echo ""
echo -e "${BLUE}下一步: 上传到服务器并部署${NC}"
echo -e "命令示例:"
echo "  scp -i ~/.ssh/singapore.pem ${OUTPUT_DIR}/*.tar.gz root@43.160.237.122:/tmp/"
echo ""
echo "⏰ 完成时间: $(date)"
