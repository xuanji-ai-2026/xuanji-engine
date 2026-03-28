import { useState } from 'react'
import { Eye, EyeOff, ShieldCheck } from 'lucide-react'
import toast from 'react-hot-toast'

export default function StealthActivation() {
  const [enabled, setEnabled] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleToggle = async () => {
    setLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setEnabled(!enabled)
    setLoading(false)
    toast.success(enabled ? '隐身模式已关闭' : '隐身模式已启用')
  }

  const features = [
    {
      title: '隐藏系统标识',
      description: '移除所有玄玑引擎品牌标识',
      icon: EyeOff,
    },
    {
      title: '自定义域名',
      description: '使用自定义域名访问管理端',
      icon: ShieldCheck,
    },
    {
      title: '隐藏管理入口',
      description: '隐藏管理端访问路径，仅可通过特定方式访问',
      icon: Eye,
    },
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          隐身激活
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          启用隐身模式以保护系统安全
        </p>
      </div>

      {/* Status Card */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              隐身模式状态
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              {enabled ? '隐身模式已启用，系统标识已隐藏' : '隐身模式未启用'}
            </p>
          </div>
          <div className="text-right">
            <div
              className={`inline-flex items-center px-4 py-2 rounded-full ${
                enabled
                  ? 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
              }`}
            >
              <div
                className={`w-2 h-2 rounded-full mr-2 ${
                  enabled ? 'bg-green-600' : 'bg-gray-600'
                }`}
              />
              {enabled ? '已启用' : '未启用'}
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={handleToggle}
            disabled={loading}
            className={`w-full py-3 rounded-lg font-medium transition-colors ${
              enabled
                ? 'bg-gray-600 hover:bg-gray-700 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            } disabled:opacity-50`}
          >
            {loading ? '处理中...' : enabled ? '关闭隐身模式' : '启用隐身模式'}
          </button>
        </div>
      </div>

      {/* Features */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          隐身功能特性
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <div className="flex items-center mb-2">
                <feature.icon className="w-5 h-5 text-blue-600 mr-2" />
                <h4 className="font-medium text-gray-900 dark:text-white">
                  {feature.title}
                </h4>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Warning */}
      {enabled && (
        <div className="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-800 rounded-xl p-6">
          <div className="flex items-start">
            <ShieldCheck className="w-5 h-5 text-yellow-600 mr-3 mt-0.5" />
            <div>
              <h4 className="font-medium text-yellow-800 dark:text-yellow-200 mb-2">
                安全提示
              </h4>
              <p className="text-sm text-yellow-700 dark:text-yellow-300">
                启用隐身模式后，请确保已妥善保存管理端访问方式。如果丢失访问方式，将无法进入管理控制台。
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
