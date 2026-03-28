import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';

const ChatHistoryPage = () => (
  <div className="space-y-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-900">对话历史</h1>
      <p className="mt-1 text-sm text-gray-600">查看所有对话记录</p>
    </div>
    <Card>
      <CardHeader>
        <CardTitle>对话列表</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500">暂无对话历史</p>
      </CardContent>
    </Card>
  </div>
);

export default ChatHistoryPage;
