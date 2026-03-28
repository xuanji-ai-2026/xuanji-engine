import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const StaffPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">工作人员管理</h1>
      <p className="mt-1 text-sm text-gray-600">管理您的工作人员和权限</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>工作人员列表</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">暂无工作人员</p>
      </CardContent>
    </Card>
  </div>
);

export default StaffPage;
