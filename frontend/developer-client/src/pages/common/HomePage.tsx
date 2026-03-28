import React from 'react';
import { Link } from 'react-router-dom';
import { Key, Puzzle, Package, MessageSquare, ArrowRight, Zap, Shield, Code } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';

export const HomePage: React.FC = () => {
  const features = [
    {
      icon: <Key className="h-8 w-8" />,
      title: 'API管理',
      description: '管理API密钥、查看调用统计、使用调试工具',
      path: '/api',
      color: 'bg-blue-100 text-blue-600',
    },
    {
      icon: <Puzzle className="h-8 w-8" />,
      title: '插件开发',
      description: '开发、测试和发布插件，访问插件市场',
      path: '/plugin',
      color: 'bg-purple-100 text-purple-600',
    },
    {
      icon: <Package className="h-8 w-8" />,
      title: 'SDK管理',
      description: '下载各平台SDK、查看集成文档',
      path: '/sdk',
      color: 'bg-green-100 text-green-600',
    },
    {
      icon: <MessageSquare className="h-8 w-8" />,
      title: '智能助手',
      description: 'AI代码生成、错误诊断、优化建议',
      path: '/assistant',
      color: 'bg-orange-100 text-orange-600',
    },
  ];

  const stats = [
    { label: 'API调用', value: '1.2M+', icon: <Zap className="h-5 w-5" /> },
    { label: '活跃插件', value: '156', icon: <Puzzle className="h-5 w-5" /> },
    { label: 'SDK下载', value: '50K+', icon: <Package className="h-5 w-5" /> },
    { label: '开发者', value: '3.2K', icon: <Code className="h-5 w-5" /> },
  ];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          欢迎使用玄玑引擎
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
          强大的AI开发平台，提供完整的工具链支持，助您快速构建智能应用
        </p>
        <div className="flex justify-center gap-4">
          <Button size="lg" icon={<ArrowRight className="h-4 w-4" />}>
            开始使用
          </Button>
          <Button variant="outline" size="lg" icon={<Code className="h-4 w-4" />}>
            查看文档
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.label}>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  {stat.icon}
                </div>
                <div>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Features */}
      <div>
        <h2 className="text-3xl font-bold text-center mb-8">核心功能</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <Link key={feature.title} to={feature.path}>
              <Card hover className="h-full">
                <CardHeader>
                  <div className={`h-12 w-12 rounded-lg ${feature.color} flex items-center justify-center mb-3`}>
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="ghost" className="w-full" icon={<ArrowRight className="h-4 w-4" />}>
                    前往
                  </Button>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              快速开始
            </CardTitle>
            <CardDescription>
              5分钟内完成第一个API调用
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <ol className="list-decimal list-inside space-y-2 text-sm">
              <li>创建API密钥</li>
              <li>下载对应平台的SDK</li>
              <li>参考集成文档配置客户端</li>
              <li>发起第一个API请求</li>
            </ol>
            <Button variant="outline" className="w-full mt-4">
              查看详细教程
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              安全与最佳实践
            </CardTitle>
            <CardDescription>
              了解如何安全地使用玄玑引擎
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <ul className="space-y-2 text-sm">
              <li className="flex items-center gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                不要在前端暴露API密钥
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                定期轮换API密钥
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                设置合理的速率限制
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                监控API调用和成本
              </li>
            </ul>
            <Button variant="outline" className="w-full mt-4">
              查看安全文档
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
