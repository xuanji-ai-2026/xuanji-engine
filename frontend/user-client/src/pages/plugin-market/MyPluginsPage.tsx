import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const MyPluginsPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">我的插件</h1>
      <p className="mt-1 text-sm text-gray-600">管理已安装的插件</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>已安装插件</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">暂无已安装的插件</p>
      </CardContent>
    </Card>
  </div>
);

export default MyPluginsPage;
