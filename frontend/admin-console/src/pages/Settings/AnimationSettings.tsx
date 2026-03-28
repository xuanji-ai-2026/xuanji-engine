import React from 'react'

export default function AnimationSettings() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">动画设置</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">配置动画效果</p>
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <p className="text-gray-600 dark:text-gray-400">动画设置模块</p>
      </div>
    </div>
  )
}
