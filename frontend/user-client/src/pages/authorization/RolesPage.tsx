import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const RolesPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">角色管理</h1>
      <p className="mt-1 text-sm text-gray-600">管理系统角色和权限分配</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>角色列表</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default RolesPage;
