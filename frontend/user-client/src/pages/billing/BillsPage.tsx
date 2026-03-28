import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const BillsPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">账单管理</h1>
      <p className="mt-1 text-sm text-gray-600">查看和管理账单</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>账单列表</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">暂无账单</p>
      </CardContent>
    </Card>
  </div>
);

export default BillsPage;
