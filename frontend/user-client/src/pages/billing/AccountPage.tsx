import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const AccountPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">账户中心</h1>
      <p className="mt-1 text-sm text-gray-600">管理您的账户信息</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>账户概览</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default AccountPage;
