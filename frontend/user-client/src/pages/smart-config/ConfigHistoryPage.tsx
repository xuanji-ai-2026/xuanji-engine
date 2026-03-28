import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const ConfigHistoryPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">配置历史</h1>
      <p className="mt-1 text-sm text-gray-600">查看和管理配置历史记录</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>历史记录</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">暂无配置历史</p>
      </CardContent>
    </Card>
  </div>
);

export default ConfigHistoryPage;
