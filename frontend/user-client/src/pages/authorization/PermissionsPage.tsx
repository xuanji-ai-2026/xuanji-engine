import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const PermissionsPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">权限管理</h1>
      <p className="mt-1 text-sm text-gray-600">管理系统权限和访问控制</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>权限列表</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default PermissionsPage;
