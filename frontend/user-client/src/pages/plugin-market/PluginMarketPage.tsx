import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import { Puzzle, Search } from 'lucide-react';

const PluginMarketPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">插件市场</h1>
      <p className="mt-1 text-sm text-gray-600">浏览和安装插件</p>
    </div>

    {/* Search */}
    <div className="relative">
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
      <input
        type="text"
        placeholder="搜索插件..."
        className="w-full rounded-lg border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
      />
    </div>

    {/* Plugins Grid */}
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <Card key={i} hover>
          <CardContent className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 mb-4">
              <Puzzle className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900">插件 {i}</h3>
            <p className="mt-1 text-sm text-gray-600">这是插件的描述信息</p>
            <div className="mt-4 flex items-center justify-between">
              <span className="text-xs text-gray-500">免费</span>
              <button className="text-sm font-medium text-primary-600 hover:text-primary-700">
                安装
              </button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  </div>
);

export default PluginMarketPage;
