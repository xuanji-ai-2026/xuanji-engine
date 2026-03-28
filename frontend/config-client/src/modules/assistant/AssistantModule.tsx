import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAssistantStore } from '@/stores/assistantStore'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/Card'
import { cn, formatRelativeTime } from '@/utils'
import { MessageSquare, Plus, Send, Sparkles, User, Bot } from 'lucide-react'

export const AssistantModule: React.FC = () => {
  const navigate = useNavigate()
  const {
    conversations,
    currentConversation,
    loading,
    sending,
    fetchConversations,
    createConversation,
    sendMessage,
    setCurrentConversation,
  } = useAssistantStore()

  const [inputMessage, setInputMessage] = useState('')
  const [showNewChat, setShowNewChat] = useState(false)

  useEffect(() => {
    fetchConversations()
  }, [fetchConversations])

  const handleNewChat = async () => {
    try {
      await createConversation('新对话')
      setShowNewChat(false)
    } catch (error) {
      console.error('Failed to create conversation:', error)
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !currentConversation || sending) return

    try {
      await sendMessage(currentConversation.id, inputMessage)
      setInputMessage('')
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  const handleSelectConversation = (conversationId: string) => {
    const conv = conversations.find((c) => c.id === conversationId)
    if (conv) {
      setCurrentConversation(conv)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">智能助手小微</h1>
          <p className="text-gray-600">配置建议、需求分析与智能引导</p>
        </div>
        <Button
          variant="primary"
          icon={<Plus className="w-4 h-4" />}
          onClick={handleNewChat}
        >
          新建对话
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Conversation List */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-lg">对话历史</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="max-h-[calc(100vh-300px)] overflow-y-auto">
              {loading ? (
                <div className="text-center py-8 text-gray-500">加载中...</div>
              ) : conversations.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-2" />
                  <p className="text-sm">暂无对话</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-200">
                  {conversations.map((conversation) => (
                    <div
                      key={conversation.id}
                      className={cn(
                        'p-4 cursor-pointer hover:bg-gray-50 transition-colors',
                        currentConversation?.id === conversation.id && 'bg-xuanji-50'
                      )}
                      onClick={() => handleSelectConversation(conversation.id)}
                    >
                      <h3 className="text-sm font-medium text-gray-900 mb-1">
                        {conversation.title}
                      </h3>
                      <p className="text-xs text-gray-500">
                        {formatRelativeTime(conversation.updatedAt)}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {conversation.messages.length} 条消息
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Chat Area */}
        <Card className="lg:col-span-3 flex flex-col h-[calc(100vh-200px)]">
          {!currentConversation ? (
            <CardContent className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <div className="w-16 h-16 bg-xuanji-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="w-8 h-8 text-xuanji-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  开始新对话
                </h3>
                <p className="text-gray-600 mb-4">
                  选择一个对话或创建新对话开始聊天
                </p>
                <Button
                  variant="primary"
                  icon={<Plus className="w-4 h-4" />}
                  onClick={handleNewChat}
                >
                  新建对话
                </Button>
              </div>
            </CardContent>
          ) : (
            <>
              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {currentConversation.messages.map((message) => (
                  <div
                    key={message.id}
                    className={cn(
                      'flex gap-3',
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    )}
                  >
                    {message.role === 'assistant' && (
                      <div className="flex-shrink-0 w-8 h-8 bg-xuanji-100 rounded-full flex items-center justify-center">
                        <Bot className="w-4 h-4 text-xuanji-600" />
                      </div>
                    )}
                    <div
                      className={cn(
                        'max-w-[70%] rounded-2xl px-4 py-2',
                        message.role === 'user'
                          ? 'bg-xuanji-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      )}
                    >
                      <p className="text-sm whitespace-pre-wrap">
                        {message.content}
                      </p>
                      {message.suggestedActions && message.suggestedActions.length > 0 && (
                        <div className="mt-3 space-y-2">
                          {message.suggestedActions.map((action, index) => (
                            <button
                              key={index}
                              className="w-full text-left px-3 py-2 bg-white bg-opacity-20 rounded-lg text-xs hover:bg-opacity-30 transition-colors"
                            >
                              {action.label}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                    {message.role === 'user' && (
                      <div className="flex-shrink-0 w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                        <User className="w-4 h-4 text-gray-600" />
                      </div>
                    )}
                  </div>
                ))}
                {sending && (
                  <div className="flex gap-3 justify-start">
                    <div className="flex-shrink-0 w-8 h-8 bg-xuanji-100 rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-xuanji-600" />
                    </div>
                    <div className="bg-gray-100 rounded-2xl px-4 py-3">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input Area */}
              <div className="border-t border-gray-200 p-4">
                <div className="flex gap-2">
                  <Input
                    placeholder="输入您的问题..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    className="flex-1"
                  />
                  <Button
                    variant="primary"
                    icon={<Send className="w-4 h-4" />}
                    onClick={handleSendMessage}
                    loading={sending}
                    disabled={!inputMessage.trim()}
                  >
                    发送
                  </Button>
                </div>
              </div>
            </>
          )}
        </Card>
      </div>
    </div>
  )
}

export default AssistantModule
