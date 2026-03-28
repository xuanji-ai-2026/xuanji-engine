import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import { Send, Mic, Paperclip, Bot } from 'lucide-react';
import { useChatStore } from '@/stores';

const ChatPage = () => {
  const [message, setMessage] = useState('');
  const { messages, currentChat, sendMessage, createChat } = useChatStore();

  const handleSend = () => {
    if (message.trim()) {
      sendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="flex h-full space-x-4">
      {/* Chat List */}
      <div className="hidden w-80 border-r border-gray-200 lg:block">
        <div className="p-4 border-b border-gray-200">
          <Button fullWidth>
            <Plus className="mr-2 h-4 w-4" />
            新建对话
          </Button>
        </div>
        <div className="space-y-1 p-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className={`rounded-lg p-3 cursor-pointer transition-colors ${
                i === 1 ? 'bg-primary-50' : 'hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100">
                  <Bot className="h-4 w-4 text-primary-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">对话 {i}</p>
                  <p className="text-xs text-gray-500 truncate">最后一条消息...</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex flex-1 flex-col rounded-lg border border-gray-200 bg-white">
        {/* Chat Header */}
        <div className="flex items-center justify-between border-b border-gray-200 p-4">
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100">
              <Bot className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">智能助手</h3>
              <p className="text-sm text-green-600">在线</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center text-gray-400">
              开始新的对话...
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg px-4 py-2 ${
                    msg.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="sm">
              <Paperclip className="h-5 w-5" />
            </Button>
            <Input
              placeholder="输入消息..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              className="flex-1"
            />
            <Button variant="ghost" size="sm">
              <Mic className="h-5 w-5" />
            </Button>
            <Button onClick={handleSend}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
