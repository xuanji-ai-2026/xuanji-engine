import React, { useState } from 'react'
import { ArrowRight, Sparkles, Brain, Database, Zap, MessageCircle, Terminal, Globe, Code, Book, Github, Mail, Star, Users, Shield, Cpu, Lock, Play, CheckCircle } from 'lucide-react'

// 主题
const theme = {
  colors: {
    primary: '#3b82f6',
    secondary: '#8b5cf6',
    accent: '#06b6d4',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    background: '#0f172a',
    surface: '#1e293b',
    text: '#f8fafc',
    textSecondary: '#94a3b8'
  }
}

// 主应用
export default function App() {
  const [view, setView] = useState('home')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  // 数字人数据
  const digitalHumans = [
    { id: 1, name: '小精灵', role: 'AI助手', desc: '可爱活泼的智能助手', rating: 4.9, users: 10000, avatar: '🧚' },
    { id: 2, name: '博士', role: '知识专家', desc: '知识渊博的学者', rating: 4.8, users: 8000, avatar: '🧙' },
    { id: 3, name: '管家', role: '生活管家', desc: '贴心周到的管家', rating: 4.7, users: 6000, avatar: '🤵' }
  ]

  // 功能数据
  const features = [
    {
      title: '智能决策',
      icon: '🧠',
      desc: '基于GPT-4，实现意图穿透式深度理解，让机器真正懂你',
      items: ['意图识别', '深度理解', '自我进化'],
      color: 'from-blue-600 to-cyan-600'
    },
    {
      title: '无限记忆',
      icon: '💾',
      desc: '支持TB级记忆，向量检索，知识图谱构建',
      items: ['向量检索', '知识图谱', '多层记忆'],
      color: 'from-green-600 to-teal-600'
    },
    {
      title: '插件生态',
      icon: '⚡',
      desc: '10万+插件库，无限扩展能力',
      items: ['插件市场', '开发者平台', 'AI生成'],
      color: 'from-yellow-600 to-orange-600'
    }
  ]

  // 定价方案
  const pricingPlans = [
    {
      name: '免费版',
      price: '¥0',
      period: '/月',
      items: ['5个AI员工', '100次/天', '基础插件', '社区支持']
    },
    {
      name: '专业版',
      price: '¥99',
      period: '/月',
      items: ['50个AI员工', '无限对话', '全部插件', 'API访问']
    },
    {
      name: '企业版',
      price: '¥999',
      period: '/月',
      items: ['200个AI员工', '专属客服', '私有部署', 'SLA保障']
    }
  ]

  return (
    <div className="min-h-screen bg-slate-900 text-white overflow-x-hidden">
      {/* 导航栏 */}
      <nav className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-lg border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="text-white w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-white">
                <span className="text-blue-400">玄玑</span><span className="text-purple-400">引擎</span>
              </span>
            </div>
            <div className="hidden md:flex items-center space-x-1">
              <button onClick={() => setView('home')} className={`text-gray-300 hover:text-white hover:bg-slate-700 rounded-lg px-4 py-2 ${view === 'home' ? 'bg-blue-600 text-white' : ''}`}>
                首页
              </button>
              <button onClick={() => setView('features')} className={`text-gray-300 hover:text-white hover:bg-slate-700 rounded-lg px-4 py-2 ${view === 'features' ? 'bg-blue-600 text-white' : ''}`}>
                功能
              </button>
              <button onClick={() => setView('humans')} className={`text-gray-300 hover:text-white hover:bg-slate-700 rounded-lg px-4 py-2 ${view === 'humans' ? 'bg-blue-600 text-white' : ''}`}>
                数字人
              </button>
              <button onClick={() => setView('pricing')} className={`text-gray-300 hover:text-white hover:bg-slate-700 rounded-lg px-4 py-2 ${view === 'pricing' ? 'bg-blue-600 text-white' : ''}`}>
                定价
              </button>
              <button onClick={() => setView('docs')} className={`text-gray-300 hover:text-white hover:bg-slate-700 rounded-lg px-4 py-2 ${view === 'docs' ? 'bg-blue-600 text-white' : ''}`}>
                文档
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容区 */}
      <div className="pt-20 px-4">
        <div className="max-w-7xl mx-auto">
          {view === 'home' && <HomeView setCurrentPage={setView} />}
          {view === 'features' && <FeaturesView features={features} />}
          {view === 'humans' && <HumansView digitalHumans={digitalHumans} setCurrentPage={setView} />}
          {view === 'pricing' && <PricingView plans={pricingPlans} />}
          {view === 'docs' && <DocsView />}
        </div>
      </div>

      {/* Footer */}
      <Footer />
    </div>
  )
}

// 首页视图
function HomeView({ setCurrentPage }) {
  const digitalHumans = [
    { id: 1, name: '小精灵', role: 'AI助手', desc: '可爱活泼的智能助手', rating: 4.9, users: 10000, avatar: '🧚' },
    { id: 2, name: '博士', role: '知识专家', desc: '知识渊博的学者', rating: 4.8, users: 8000, avatar: '🧙' },
    { id: 3, name: '管家', role: '生活管家', desc: '贴心周到的管家', rating: 4.7, users: 6000, avatar: '🤵' }
  ]

  const features = [
    {
      title: '智能决策',
      icon: '🧠',
      desc: '基于GPT-4，实现意图穿透式深度理解，让机器真正懂你',
      items: ['意图识别', '深度理解', '自我进化'],
      color: 'from-blue-600 to-cyan-600'
    },
    {
      title: '无限记忆',
      icon: '💾',
      desc: '支持TB级记忆，向量检索，知识图谱构建',
      items: ['向量检索', '知识图谱', '多层记忆'],
      color: 'from-green-600 to-teal-600'
    },
    {
      title: '插件生态',
      icon: '⚡',
      desc: '10万+插件库，无限扩展能力',
      items: ['插件市场', '开发者平台', 'AI生成'],
      color: 'from-yellow-600 to-orange-600'
    }
  ]

  return (
    <div className="min-h-screen flex items-center justify-center px-4 pt-20 pb-20">
      <div className="max-w-5xl mx-auto text-center">
        {/* Hero区域 */}
        <div className="mb-16">
          <div className="inline-block px-4 py-2 bg-blue-600/20 border border-blue-500/30 rounded-full text-blue-400 text-sm font-medium mb-6">
            <Star className="w-4 h-4 mr-1" />
            AI十星曜架构大型数字人引擎
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-4">
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              打造你的AI数字员工
            </span>
          </h1>

          <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
            安全可靠 · 智能协作 · 无限可能
          </p>

          {/* CTA按钮 */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <button
              onClick={() => setCurrentPage('humans')}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl text-white font-semibold hover:opacity-90 transition-opacity"
            >
              选择数字人
              <ArrowRight className="ml-2 w-5 h-5" />
            </button>
          </div>

          {/* 统计数据 */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {[
              { value: '500,000+', label: '代码行数', icon: <Code className="w-4 h-4" /> },
              { value: '100,000+', label: '插件数量', icon: <Zap className="w-4 h-4" /> },
              { value: '150+', label: 'API接口', icon: <Terminal className="w-4 h-4" /> },
              { value: '99.9%', label: '可用性', icon: <CheckCircle className="w-4 h-4" /> }
            ].map((stat, i) => (
              <div key={i} className="p-4 bg-slate-800/50 border-slate-700 rounded-2xl">
                <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-gray-500 text-sm flex items-center gap-2">
                  {React.cloneElement(stat.icon, { className: 'w-4 h-4' })}
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 功能展示 */}
        <div className="py-20 px-4 bg-slate-900/50">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-4 text-white">
              核心能力
            </h2>
            <p className="text-center text-gray-400 text-lg mb-12">
              十星曜架构，全面领先
            </p>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, i) => (
                <div
                  key={i}
                  className="p-6 rounded-2xl bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:-translate-y-1 transition-all"
                >
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-2xl mb-4`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-gray-400 text-sm mb-4">{feature.desc}</p>
                  <div className="flex flex-wrap gap-2">
                    {feature.items.map((item, j) => (
                      <span key={j} className="px-3 py-1 bg-slate-700/50 rounded-full text-xs text-gray-400">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 数字人展示 */}
        <div className="py-20 px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-4 text-white">
              选择你的<span className="text-purple-400">数字人</span>
            </h2>
            <p className="text-gray-400 text-lg mb-12">
              {digitalHumans.length}个数字人可选，满足各种场景需求
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {digitalHumans.map(human => (
                <div
                  key={human.id}
                  onClick={() => alert('对话功能开发中...')}
                  className="p-6 rounded-2xl bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:-translate-y-1 transition-all cursor-pointer"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="text-5xl mb-3">{human.avatar}</div>
                    <div className="flex items-center gap-2">
                      <Star className="w-4 h-4 text-yellow-400 mr-1" />
                      <span className="text-yellow-400 text-xl font-bold">{human.rating}</span>
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-1">{human.name}</h3>
                  <p className="text-purple-400 text-sm mb-2">{human.role}</p>
                  <p className="text-gray-400 text-sm">{human.desc}</p>
                  <div className="flex items-center justify-between mt-4">
                    <div className="flex items-center text-yellow-400 text-sm">
                      <Star className="w-4 h-4 mr-1" />
                      <span>{human.rating}</span>
                    </div>
                    <span className="text-gray-500 text-sm">{human.users.toLocaleString()}用户</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// 功能视图
function FeaturesView({ features }) {
  return (
    <div className="py-20 px-4 bg-slate-900/50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-4 text-white">
          核心能力
        </h2>
        <p className="text-center text-gray-400 text-lg mb-12">
          十星曜架构，全面领先
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:-translate-y-1 transition-all"
            >
              <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-2xl mb-4`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-gray-400 text-sm mb-4">{feature.desc}</p>
              <div className="flex flex-wrap gap-2">
                {feature.items.map((item, j) => (
                  <span key={j} className="px-3 py-1 bg-slate-700/50 rounded-full text-xs text-gray-400">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// 数字人视图
function HumansView({ digitalHumans, setCurrentPage }) {
  const [filter, setFilter] = useState('全部')

  return (
    <div className="min-h-screen bg-slate-900 py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-4 text-white">
          选择你的<span className="text-purple-400">数字人</span>
        </h2>
        <p className="text-gray-400 text-lg mb-8">
          {digitalHumans.length}个数字人可选
        </p>

        {/* 分类筛选 */}
        <div className="flex flex-wrap justify-center gap-2 mb-8">
          {['全部', '助手', '教育', '服务', '创意'].map((cat, i) => (
            <button
              key={i}
              onClick={() => setFilter(cat)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                filter === cat
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 text-gray-300 hover:text-white hover:bg-slate-600'
              }`}
            >
              {cat} ({digitalHumans.filter(h => h.category === cat).length})
            </button>
          ))}
        </div>

        {/* 数字人列表 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
          {digitalHumans.map(human => (
            <div
              key={human.id}
              className="p-6 rounded-2xl bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:-translate-y-1 cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="text-5xl mb-3">{human.avatar}</div>
                <div className="flex items-center gap-2">
                  <Star className="w-4 h-4 text-yellow-400 mr-1" />
                  <span className="text-yellow-400 text-xl font-bold">{human.rating}</span>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-1">{human.name}</h3>
              <p className="text-purple-400 text-sm mb-2">{human.role}</p>
              <p className="text-gray-400 text-sm">{human.desc}</p>
              <div className="flex items-center justify-between mt-4">
                <div className="flex items-center text-yellow-400 text-sm">
                  <Star className="w-4 h-4 mr-1" />
                  <span>{human.rating}</span>
                </div>
                <span className="text-gray-500 text-sm">{human.users.toLocaleString()}用户</span>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center">
          <button
            className="inline-flex items-center px-6 py-3 bg-white/10 border border-white/20 rounded-xl text-white hover:bg-white/20 transition-colors"
          >
            查看全部数字人（{digitalHumans.length}+）
          </button>
        </div>
      </div>
    </div>
  )
}

// 定价视图
function PricingView({ plans }) {
  return (
    <div className="py-20 px-4 bg-slate-900/50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-4 text-white">
          灵活的<span className="text-green-400">定价</span>
        </h2>
        <p className="text-gray-400 text-lg mb-12">
          根据需求选择合适的方案
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {plans.map((plan, i) => (
            <div
              key={i}
              className={`relative p-6 rounded-2xl bg-slate-800/50 border ${
                plan.name === '专业版' ? 'border-purple-500 ring-2 ring-purple-500' : 'border-slate-700'
              } transition-all hover:-translate-y-1`}
            >
              {plan.name === '专业版' && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full text-xs font-medium text-white">
                  最受欢迎
                </div>
              )}
              <div className="flex items-center justify-center mb-4">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${plan.name === '免费版' ? 'from-slate-600 to-slate-700' : plan.name === '专业版' ? 'from-blue-600 to-purple-600' : 'from-purple-600 to-pink-600'} flex items-center justify-center text-2xl text-white`}>
                  <Zap className="w-8 h-8" />
                </div>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-2">
                {plan.name}
              </h3>
              <div className="mb-2">
                <span className="text-4xl font-bold text-white">{plan.price}</span>
                <span className="text-gray-400 text-lg">{plan.period}</span>
              </div>
              <p className="text-gray-400 text-sm mb-6">{plan.description}</p>
              <ul className="space-y-3 mb-6">
                {plan.items.map((item, j) => (
                  <li key={j} className="flex items-center text-slate-300 text-sm">
                    <CheckCircle className="w-4 h-4 mr-2 text-green-400" />
                    {item}
                  </li>
                ))}
              </ul>
              <button
                className={`w-full py-3 rounded-xl font-medium transition-all ${
                  plan.name === '专业版'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:opacity-90'
                    : 'bg-slate-700 text-white hover:bg-slate-600'
                }`}
              >
                {plan.name === '免费版' ? '免费开始' : plan.name === '专业版' ? '立即购买' : '联系我们'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// 文档视图
function DocsView() {
  const docs = [
    {
      title: '用户手册',
      icon: '📖',
      desc: '快速上手指南、最佳实践、API文档'
    },
    {
      title: '开发者指南',
      icon: '💻',
      desc: 'SDK下载、插件开发、API密钥'
    },
    {
      title: 'API文档',
      icon: '📋',
      desc: 'REST API、WebSocket、Webhooks'
    },
    {
      title: '开源社区',
      icon: '🤝',
      desc: '技术交流、问题反馈、社区交流'
    }
  ]

  return (
    <div className="py-20 px-4 bg-slate-900/50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-4 text-white">
          <span className="text-blue-400">文档</span>中心
        </h2>
        <p className="text-gray-400 text-lg mb-12">
          完整的开发文档和资源
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {docs.map((doc, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:-translate-y-1 transition-all cursor-pointer"
            >
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-2xl mb-4">
                {doc.icon}
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{doc.title}</h3>
              <p className="text-gray-400 text-sm mb-4">{doc.desc}</p>
              <div className="flex items-center text-blue-400 text-sm mt-4">
                查看详情 →
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// Footer组件
function Footer() {
  return (
    <footer className="py-12 px-4 border-t border-slate-800 bg-slate-900">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="text-white w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-white">玄玑引擎</span>
            </div>
            <p className="text-slate-400 text-sm">AI十星曜架构大型数字人引擎</p>
          </div>
          <div>
            <h4 className="text-white font-medium mb-4">产品</h4>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">功能介绍</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">定价方案</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">数字人</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-4">公司</h4>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">关于我们</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">博客</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">联系方式</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-4">资源</h4>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">API文档</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">开发者文档</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">开源社区</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800 text-center text-gray-500 text-sm">
          © 2026 玄玑AI. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
