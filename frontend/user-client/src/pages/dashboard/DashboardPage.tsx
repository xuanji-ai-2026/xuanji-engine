import { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import { useDigitalHumanStore } from '@/stores';
import Loading from '@/components/common/Button';
import {
  Bot,
  MessageSquare,
  Activity,
  CreditCard,
  TrendingUp,
  Users,
} from 'lucide-react';

const DashboardPage = () => {
  const { digitalHumans, fetchDigitalHumans, isLoading } = useDigitalHumanStore();

  useEffect(() => {
    fetchDigitalHumans();
  }, [fetchDigitalHumans]);

  const stats = [
    {
      title: '数字人数量',
      value: digitalHumans.length,
      icon: Bot,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'increase' as const,
    },
    {
      title: '对话次数',
      value: '1,234',
      icon: MessageSquare,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'increase' as const,
    },
    {
      title: '活跃度',
      value: '85%',
      icon: Activity,
      color: 'bg-purple-500',
      change: '+5%',
      changeType: 'increase' as const,
    },
    {
      title: '账户余额',
      value: '¥2,580',
      icon: CreditCard,
      color: 'bg-orange-500',
      change: '-3%',
      changeType: 'decrease' as const,
    },
  ];

  const recentActivity = [
    { id: 1, action: '创建了数字人', target: '小助手', time: '5分钟前' },
    { id: 2, action: '进行了对话', target: '客服助手', time: '15分钟前' },
    { id: 3, action: '更新了配置', target: '智能问答', time: '1小时前' },
    { id: 4, action: '安装了插件', target: '翻译插件', time: '2小时前' },
    { id: 5, action: '完成了充值', target: '账户余额', time: '3小时前' },
  ];

  if (isLoading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">仪表盘</h1>
        <p className="mt-1 text-sm text-gray-600">欢迎回来，查看您的应用概览</p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title} hover>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="mt-2 text-2xl font-bold text-gray-900">
                    {stat.value}
                  </p>
                  <p
                    className={`mt-1 text-sm ${
                      stat.changeType === 'increase'
                        ? 'text-green-600'
                        : 'text-red-600'
                    }`}
                  >
                    {stat.change}
                  </p>
                </div>
                <div
                  className={`flex h-12 w-12 items-center justify-center rounded-lg ${stat.color}`}
                >
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Digital Humans */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>最近创建的数字人</CardTitle>
              <a href="/digital-humans" className="text-sm text-primary-600 hover:text-primary-700">
                查看全部
              </a>
            </div>
          </CardHeader>
          <CardContent>
            {digitalHumans.length === 0 ? (
              <p className="py-8 text-center text-gray-500">暂无数字人</p>
            ) : (
              <div className="space-y-3">
                {digitalHumans.slice(0, 5).map((dh) => (
                  <div
                    key={dh.id}
                    className="flex items-center justify-between rounded-lg border border-gray-200 p-3 hover:bg-gray-50"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100">
                        <Bot className="h-5 w-5 text-primary-600" />
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{dh.displayName}</p>
                        <p className="text-sm text-gray-500">{dh.status}</p>
                      </div>
                    </div>
                    <span className="text-xs text-gray-400">
                      {new Date(dh.createdAt).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>最近活动</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-start space-x-3"
                >
                  <div className="mt-1 h-2 w-2 rounded-full bg-primary-600" />
                  <div className="flex-1">
                    <p className="text-sm text-gray-900">
                      {activity.action} <span className="font-medium">{activity.target}</span>
                    </p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
