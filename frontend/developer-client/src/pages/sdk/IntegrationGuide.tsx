import React, { useState } from 'react';
import { Copy, CheckCircle, Code, Terminal, Globe, Key } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useCopyToClipboard } from '../../hooks/useCopyToClipboard';

export const IntegrationGuide: React.FC = () => {
  const [selectedPlatform, setSelectedPlatform] = useState('javascript');
  const [, copy] = useCopyToClipboard();

  const platforms = [
    { value: 'javascript', label: 'JavaScript', icon: '⚡' },
    { value: 'python', label: 'Python', icon: '🐍' },
    { value: 'java', label: 'Java', icon: '☕' },
    { value: 'go', label: 'Go', icon: '🐹' },
  ];

  const quickStart = `
## 快速开始

### 1. 安装SDK

\`\`\`bash
npm install @xuanji/sdk
\`\`\`

### 2. 初始化客户端

\`\`\`javascript
import { XuanjiClient } from '@xuanji/sdk';

const client = new XuanjiClient({
  apiKey: 'your-api-key',
  endpoint: 'https://api.xuanji.ai'
});
\`\`\`

### 3. 发起请求

\`\`\`javascript
const result = await client.chat.completions.create({
  model: 'xuanji-v2',
  messages: [
    { role: 'user', content: '你好！' }
  ]
});

console.log(result.choices[0].message.content);
\`\`\`
`;

  const integrationSteps = [
    {
      step: 1,
      title: '获取API密钥',
      description: '在开发者控制台创建新的API密钥',
      icon: <Key className="h-5 w-5" />,
    },
    {
      step: 2,
      title: '安装SDK',
      description: '使用包管理器安装对应平台的SDK',
      icon: <Terminal className="h-5 w-5" />,
    },
    {
      step: 3,
      title: '配置客户端',
      description: '使用API密钥初始化客户端',
      icon: <Code className="h-5 w-5" />,
    },
    {
      step: 4,
      title: '发起请求',
      description: '调用API接口处理业务逻辑',
      icon: <Globe className="h-5 w-5" />,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">集成指南</h2>
        <p className="text-muted-foreground">分步指南帮助您快速集成玄玑引擎SDK</p>
      </div>

      {/* Platform Selector */}
      <div className="flex gap-2">
        {platforms.map((platform) => (
          <Button
            key={platform.value}
            variant={selectedPlatform === platform.value ? 'primary' : 'outline'}
            onClick={() => setSelectedPlatform(platform.value)}
          >
            <span className="mr-2">{platform.icon}</span>
            {platform.label}
          </Button>
        ))}
      </div>

      {/* Integration Steps */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {integrationSteps.map((step) => (
          <Card key={step.step}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  {step.icon}
                </div>
                <div>
                  <CardTitle className="text-base">步骤 {step.step}</CardTitle>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <h4 className="font-semibold mb-1">{step.title}</h4>
              <p className="text-sm text-muted-foreground">{step.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Start */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>快速开始</CardTitle>
              <CardDescription>5分钟内完成SDK集成</CardDescription>
            </div>
            <Button variant="ghost" size="sm" icon={<Copy className="h-4 w-4" />} />
          </div>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <div className="relative">
                      <SyntaxHighlighter
                        language={match[1]}
                        style={vscDarkPlus}
                        customStyle={{ borderRadius: '8px' }}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    </div>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {quickStart}
            </ReactMarkdown>
          </div>
        </CardContent>
      </Card>

      {/* Examples */}
      <Card>
        <CardHeader>
          <CardTitle>示例代码</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="basic">
            <TabsList>
              <TabsTrigger value="basic">基础用法</TabsTrigger>
              <TabsTrigger value="advanced">高级功能</TabsTrigger>
              <TabsTrigger value="error">错误处理</TabsTrigger>
            </TabsList>

            <TabsContent value="basic" className="mt-4">
              <SyntaxHighlighter
                language="typescript"
                style={vscDarkPlus}
                customStyle={{ borderRadius: '8px' }}
              >
{`// 基础对话示例
import { XuanjiClient } from '@xuanji/sdk';

const client = new XuanjiClient({
  apiKey: process.env.XUANJI_API_KEY
});

async function chat(prompt: string) {
  const response = await client.chat.completions.create({
    model: 'xuanji-v2',
    messages: [{ role: 'user', content: prompt }]
  });
  return response.choices[0].message.content;
}`}
              </SyntaxHighlighter>
            </TabsContent>

            <TabsContent value="advanced" className="mt-4">
              <SyntaxHighlighter
                language="typescript"
                style={vscDarkPlus}
                customStyle={{ borderRadius: '8px' }}
              >
{`// 流式响应和配置
async function streamChat() {
  const stream = await client.chat.completions.create({
    model: 'xuanji-v2',
    messages: [{ role: 'user', content: '写一首诗' }],
    stream: true,
    temperature: 0.8,
    maxTokens: 500
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}`}
              </SyntaxHighlighter>
            </TabsContent>

            <TabsContent value="error" className="mt-4">
              <SyntaxHighlighter
                language="typescript"
                style={vscDarkPlus}
                customStyle={{ borderRadius: '8px' }}
              >
{`// 完整的错误处理
import { XuanjiError } from '@xuanji/sdk';

try {
  const result = await client.chat.completions.create({
    model: 'xuanji-v2',
    messages: [{ role: 'user', content: 'Hello' }]
  });
} catch (error) {
  if (error instanceof XuanjiError) {
    console.error('API Error:', error.message);
    console.error('Status:', error.status);
    console.error('Code:', error.code);
  } else {
    console.error('Unknown error:', error);
  }
}`}
              </SyntaxHighlighter>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};
