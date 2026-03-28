import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const EmotionConfigPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">情绪配置</h1>
      <p className="mt-1 text-sm text-gray-600">配置数字人的情绪表达</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>情绪设置</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">配置加载中...</p>
      </CardContent>
    </Card>
  </div>
);

export default EmotionConfigPage;
