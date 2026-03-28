import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import Button from '@/components/common/Button';
import { Plus, Bot, Search, Filter } from 'lucide-react';

const DigitalHumanListPage = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">数字人管理</h1>
          <p className="mt-1 text-sm text-gray-600">创建和管理您的AI数字人</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          创建数字人
        </Button>
      </div>

      {/* Search and Filter */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center space-x-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="搜索数字人..."
                className="w-full rounded-lg border border-gray-300 bg-gray-50 py-2 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none"
              />
            </div>
            <Button variant="outline">
              <Filter className="mr-2 h-4 w-4" />
              筛选
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Digital Humans Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <Card key={i} hover>
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary-100">
                  <Bot className="h-8 w-8 text-primary-600" />
                </div>
                <span className="inline-flex items-center rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-800">
                  活跃
                </span>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">数字人 {i}</h3>
              <p className="mt-1 text-sm text-gray-600">这是数字人的描述信息</p>
              <div className="mt-4 flex items-center justify-between">
                <span className="text-xs text-gray-500">创建于 2024-03-{i + 20}</span>
                <Button variant="ghost" size="sm">
                  管理
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default DigitalHumanListPage;
