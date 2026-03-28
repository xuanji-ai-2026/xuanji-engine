import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const PersonalityConfigPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">人格配置</h1>
      <p className="mt-1 text-sm text-gray-600">配置数字人的性格特征</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>人格设置</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">配置加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default PersonalityConfigPage;
