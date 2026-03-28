import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const DigitalHumanDetailPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">数字人详情</h1>
      <p className="mt-1 text-sm text-gray-600">查看和管理数字人详细信息</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>详细信息</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default DigitalHumanDetailPage;
