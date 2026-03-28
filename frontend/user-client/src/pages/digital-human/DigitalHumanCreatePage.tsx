import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const DigitalHumanCreatePage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">创建数字人</h1>
      <p className="mt-1 text-sm text-gray-600">创建新的AI数字人</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>创建向导</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">选择创建方式</p>
      </CardContent>
    </Card>
  </div>
);

export default DigitalHumanCreatePage;
