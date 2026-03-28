import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const RechargePage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">充值</h1>
      <p className="mt-1 text-sm text-gray-600">为账户充值</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>充值方式</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default RechargePage;
