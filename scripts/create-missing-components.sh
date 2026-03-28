#!/bin/bash

# 创建缺失的组件占位符

CLIENT_DIR="/workspace/projects/workspace/xuanji-engine-v2/frontend/config-client"

# 组件列表
declare -A COMPONENTS=(
  ["${CLIENT_DIR}/src/modules/user/components/UserProfileEdit.tsx"]="UserProfileEdit"
  ["${CLIENT_DIR}/src/modules/user/components/UserProfileView.tsx"]="UserProfileView"
  ["${CLIENT_DIR}/src/modules/digitalhuman/components/DigitalHumanConfigWizard.tsx"]="DigitalHumanConfigWizard"
  ["${CLIENT_DIR}/src/modules/digitalhuman/components/TemplateSelector.tsx"]="TemplateSelector"
)

COMPONENT_TEMPLATE='import React from "react"

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

for file in "${!COMPONENTS[@]}"; do
  component_name="${COMPONENTS[$file]}"
  echo "Creating: $file"
  mkdir -p "$(dirname "$file")"
  echo "${COMPONENT_TEMPLATE//COMPONENT_NAME/$component_name}" > "$file"
done

echo "✅ 组件创建完成"
