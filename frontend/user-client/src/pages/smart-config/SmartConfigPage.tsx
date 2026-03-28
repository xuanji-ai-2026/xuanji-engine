import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import Button from '@/components/common/Button';
import { Bot, MessageCircle, Sparkles, History } from 'lucide-react';

const SmartConfigPage = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '你好！我是智能配置助手。请告诉我您想要创建什么样的数字人？' },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage = {
        role: 'assistant',
        content: `收到您的需求：${input}\n\n让我们一步步来完成配置。首先，请告诉我这个数字人的主要用途是什么？`,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      {/* Main Chat Area */}
      <div className="lg:col-span-2">
        <Card className="h-[calc(100vh-200px)]">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center">
                <Sparkles className="mr-2 h-5 w-5 text-primary-600" />
                智能配置
              </CardTitle>
              <Button variant="outline" size="sm">
                <History className="mr-2 h-4 w-4" />
                配置历史
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex flex-col h-full">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 mb-4">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 ${
                      msg.role === 'user'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-3">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input */}
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="描述您的需求..."
                className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
              />
              <Button onClick={handleSend}>
                <MessageCircle className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sidebar */}
      <div className="space-y-4">
        {/* Progress */}
        <Card>
          <CardHeader>
            <CardTitle>配置进度</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>基本信息</span>
                  <span className="text-green-600">已完成</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 w-full" />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>人格设置</span>
                  <span className="text-primary-600">进行中</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-primary-500 w-1/2" />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>情绪配置</span>
                  <span className="text-gray-400">待开始</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-gray-300 w-0" />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>插件选择</span>
                  <span className="text-gray-400">待开始</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-gray-300 w-0" />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>快速操作</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" fullWidth>
              使用模板
            </Button>
            <Button variant="outline" fullWidth>
              保存草稿
            </Button>
            <Button variant="outline" fullWidth>
              重新开始
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SmartConfigPage;
