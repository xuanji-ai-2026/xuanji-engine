import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const PluginConfigPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">插件配置</h1>
      <p className="mt-1 text-sm text-gray-600">配置数字人使用的插件</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>插件管理</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default PluginConfigPage;
