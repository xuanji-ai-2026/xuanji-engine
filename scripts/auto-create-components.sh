#!/bin/bash

set -e

CLIENT_DIR="/workspace/projects/workspace/xuanji-engine-v2/frontend/config-client"

# 定义所有缺失的组件
declare -A COMPONENTS=(
  ["${CLIENT_DIR}/src/modules/user/components/UserProfileEdit.tsx"]="UserProfileEdit"
  ["${CLIENT_DIR}/src/modules/user/components/UserProfileView.tsx"]="UserProfileView"
  ["${CLIENT_DIR}/src/modules/user/components/UserList.tsx"]="UserList"
  ["${CLIENT_DIR}/src/modules/digitalhuman/components/DigitalHumanConfigWizard.tsx"]="DigitalHumanConfigWizard"
  ["${CLIENT_DIR}/src/modules/digitalhuman/components/TemplateSelector.tsx"]="TemplateSelector"
  ["${CLIENT_DIR}/src/modules/digitalhuman/components/DigitalHumanList.tsx"]="DigitalHumanList"
  ["${CLIENT_DIR}/src/modules/knowledge/components/KnowledgeBaseManage.tsx"]="KnowledgeBaseManage"
  ["${CLIENT_DIR}/src/modules/knowledge/components/DocumentUpload.tsx"]="DocumentUpload"
  ["${CLIENT_DIR}/src/modules/plugin/components/PluginList.tsx"]="PluginList"
  ["${CLIENT_DIR}/src/modules/plugin/components/PluginManage.tsx"]="PluginManage"
)

COMPONENT_SIMPLE='import React from "react"

const COMPONENT_NAME: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">COMPONENT_NAME</h1>
      <p className="text-gray-600">功能开发中</p>
    </div>
  )
}

export default COMPONENT_NAME
'

COMPONENT_WITH_PARAMS='import React from "react"
import { useParams } from "react-router-dom"

const COMPONENT_NAME: React.FC = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">COMPONENT_NAME</h1>
      <p className="text-gray-600">ID: {id}</p>
      <p className="text-gray-600 mt-4">功能开发中</p>
    </div>
  )
}

export default COMPONENT_NAME
'

# 带参数的组件
PARAMS_COMPONENTS=(
  "UserProfileEdit"
  "UserProfileView"
  "DigitalHumanConfigWizard"
  "TemplateSelector"
  "KnowledgeBaseManage"
  "DocumentUpload"
  "PluginManage"
)

count=0
for file in "${!COMPONENTS[@]}"; do
  component_name="${COMPONENTS[$file]}"
  
  # 检查文件是否已存在
  if [ -f "$file" ]; then
    echo "⏭️  跳过已存在: $(basename $file)"
    continue
  fi
  
  mkdir -p "$(dirname "$file")"
  
  # 使用带参数的组件模板
  if [[ " ${PARAMS_COMPONENTS[@]} " =~ " ${component_name} " ]]; then
    echo "${COMPONENT_WITH_PARAMS//COMPONENT_NAME/$component_name}" > "$file"
  else
    echo "${COMPONENT_SIMPLE//COMPONENT_NAME/$component_name}" > "$file"
  fi
  
  echo "✅ 创建: $(basename $file)"
  ((count++))
done

echo ""
echo "🎉 共创建 $count 个组件"
