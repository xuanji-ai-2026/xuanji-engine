import { useState } from 'react'

export const features = [
  {
    title: '智能理解',
    description: '深度语言理解，精准把握用户意图',
    icon: '🧠',
  },
  {
    title: '多模态交互',
    description: '支持文本、语音、图像等多种交互方式',
    icon: '🎤',
  },
  {
    title: '安全可靠',
    description: '企业级安全防护，等保三级认证',
    icon: '🛡️',
  },
  {
    title: '插件生态',
    description: '10万+级插件库，无限扩展可能',
    icon: '🔌',
  },
]

export const scenarios = [
  {
    title: '个人用户',
    description: '智能助手、学习辅导、生活管理',
    icon: '👤',
    items: ['智能对话助手', '个性化学习', '日程管理', '健康管理'],
  },
  {
    title: '企业服务',
    description: '客服机器人、数据分析、流程自动化',
    icon: '🏢',
    items: ['智能客服', '数据分析', '流程自动化', '决策支持'],
  },
  {
    title: '行业应用',
    description: '金融、医疗、教育、零售等垂直领域',
    icon: '🏭',
    items: ['金融风控', '医疗辅助', '教育培训', '零售导购'],
  },
  {
    title: '政府机构',
    description: '政务服务、城市治理、民生服务',
    icon: '🏛️',
    items: ['智能政务', '城市治理', '民生服务', '应急响应'],
  },
]

export const stats = [
  { value: '10万+', label: '插件数量' },
  { value: '99.9%', label: '准确率' },
  { value: '24/7', label: '在线服务' },
  { value: '等保三级', label: '安全认证' },
]
