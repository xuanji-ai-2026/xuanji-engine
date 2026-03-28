import { useState } from 'react'
import { CheckCircle, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'

export default function CreatorBinding() {
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)

  const handleNext = async () => {
    setLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setStep(step + 1)
    setLoading(false)
  }

  const steps = [
    {
      title: '创建创始人账户',
      description: '设置创始人邮箱、密码和基本信息',
      content: <AccountForm />,
    },
    {
      title: '验证身份',
      description: '通过邮箱验证创始人身份',
      content: <VerificationForm />,
    },
    {
      title: '完成绑定',
      description: '创始人账户绑定成功',
      content: <CompletionStep />,
    },
  ]

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          创始人绑定
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          完成创始人账户绑定流程
        </p>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((s, index) => (
            <div key={index} className="flex items-center flex-1">
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    index + 1 <= step
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                  }`}
                >
                  {index + 1 < step ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <span className="text-sm font-medium">{index + 1}</span>
                  )}
                </div>
                <div className="mt-2 text-center">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {s.title}
                  </p>
                </div>
              </div>
              {index < steps.length - 1 && (
                <div className="flex-1 h-0.5 mx-4">
                  <div
                    className={`h-full transition-colors ${
                      index + 1 < step ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
                    }`}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Current Step */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            {steps[step - 1]?.title || '步骤未找到'}
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {steps[step - 1]?.description || ''}
          </p>
        </div>
        {steps[step - 1]?.content || <div>内容加载中...</div>}

        {step < steps.length && (
          <div className="mt-8 flex justify-end">
            <button
              onClick={handleNext}
              disabled={loading}
              className="flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50"
            >
              {loading ? '处理中...' : '下一步'}
              <ArrowRight className="w-4 h-4 ml-2" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function AccountForm() {
  return (
    <form className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            姓名
          </label>
          <input
            type="text"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
            placeholder="请输入姓名"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            邮箱
          </label>
          <input
            type="email"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
            placeholder="请输入邮箱"
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          密码
        </label>
        <input
          type="password"
          className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
          placeholder="请输入密码"
        />
      </div>
    </form>
  )
}

function VerificationForm() {
  const [code, setCode] = useState('')

  const handleVerify = () => {
    toast.success('验证成功')
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          我们已向您的邮箱发送了验证码，请输入验证码完成身份验证
        </p>
        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          maxLength={6}
          className="w-64 px-4 py-3 text-center text-2xl tracking-widest border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
          placeholder="000000"
        />
      </div>
      <div className="text-center">
        <button
          onClick={handleVerify}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
        >
          验证
        </button>
      </div>
    </div>
  )
}

function CompletionStep() {
  return (
    <div className="text-center py-12">
      <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mb-4">
        <CheckCircle className="w-8 h-8 text-green-600" />
      </div>
      <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
        绑定成功
      </h3>
      <p className="text-gray-600 dark:text-gray-400">
        创始人账户已成功绑定，您现在可以开始使用系统
      </p>
    </div>
  )
}
