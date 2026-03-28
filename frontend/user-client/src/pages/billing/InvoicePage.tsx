import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const InvoicePage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">发票管理</h1>
      <p className="mt-1 text-sm text-gray-600">申请和管理发票</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>发票列表</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">暂无发票</p>
      </CardContent>
    </Card>
  </div>
);

export default InvoicePage;
