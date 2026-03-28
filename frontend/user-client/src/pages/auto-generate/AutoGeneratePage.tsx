import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const AutoGeneratePage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">自动配置生成</h1>
      <p className="mt-1 text-sm text-gray-600">AI自动生成数字人配置</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>生成向导</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">选择配置类型开始生成</p>
      </CardContent>
    </Card>
  </div>
);

export default AutoGeneratePage;
