import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import Button from '@/components/common/Button';
import { Sparkles, MessageCircle, Mic, Send } from 'lucide-react';
import { useAssistantStore } from '@/stores';

const AssistantPage = () => {
  const [input, setInput] = useState('');
  const { messages, sendMessage, isTyping } = useAssistantStore();

  const handleSend = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-purple-100 mb-4">
          <Sparkles className="h-8 w-8 text-purple-600" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900">小紫助手</h1>
        <p className="mt-1 text-sm text-gray-600">您的智能助手，随时为您服务</p>
      </div>

      <Card>
        <CardContent className="p-6">
          {/* Messages */}
          <div className="h-[400px] overflow-y-auto space-y-4 mb-4">
            {messages.length === 0 && (
              <div className="flex h-full items-center justify-center text-gray-400">
                <div className="text-center">
                  <MessageCircle className="mx-auto h-12 w-12 mb-2" />
                  <p>开始与小紫对话吧！</p>
                </div>
              </div>
            )}
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    msg.role === 'user'
                      ? 'bg-purple-600 text-white'
                      : 'bg-purple-50 text-gray-900'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-purple-50 rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm">
              <Mic className="h-4 w-4" />
            </Button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="向小紫提问..."
              className="flex-1 rounded-full border border-gray-300 bg-white px-4 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20"
            />
            <Button onClick={handleSend} className="rounded-full">
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AssistantPage;
