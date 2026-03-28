import React, { useState } from 'react';
import { Code, Sparkles, Copy, Download } from 'lucide-react';
import { Button } from '../../components/Button';
import { Input } from '../../components/Input';
import { Textarea } from '../../components/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { useAssistantStore } from '../../stores/assistantStore';
import { useCopyToClipboard } from '../../hooks/useCopyToClipboard';
import Editor from '@monaco-editor/react';

export const CodeGenerator: React.FC = () => {
  const { codeResult, loading, generateCode } = useAssistantStore();
  const [description, setDescription] = useState('');
  const [language, setLanguage] = useState('typescript');
  const [context, setContext] = useState('');
  const [, copy] = useCopyToClipboard();

  const languages = [
    { value: 'typescript', label: 'TypeScript' },
    { value: 'javascript', label: 'JavaScript' },
    { value: 'python', label: 'Python' },
    { value: 'java', label: 'Java' },
    { value: 'go', label: 'Go' },
  ];

  const handleGenerate = async () => {
    await generateCode(description, language);
  };

  const handleCopy = () => {
    if (codeResult?.code) {
      copy(codeResult.code);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">代码生成</h2>
        <p className="text-muted-foreground">使用AI生成高质量代码</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Input Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              配置参数
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">功能描述</label>
              <Textarea
                placeholder="描述您需要实现的功能，例如：创建一个用户认证中间件，支持JWT验证和角色检查"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={4}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">编程语言</label>
              <div className="flex gap-2">
                {languages.map((lang) => (
                  <Button
                    key={lang.value}
                    variant={language === lang.value ? 'primary' : 'outline'}
                    size="sm"
                    onClick={() => setLanguage(lang.value)}
                  >
                    {lang.label}
                  </Button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">上下文 (可选)</label>
              <Textarea
                placeholder="提供相关代码上下文，帮助AI更好地理解需求"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                rows={3}
              />
            </div>

            <Button
              className="w-full"
              onClick={handleGenerate}
              loading={loading}
              disabled={!description.trim()}
              icon={<Sparkles className="h-4 w-4" />}
            >
              生成代码
            </Button>
          </CardContent>
        </Card>

        {/* Output Panel */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg flex items-center gap-2">
                <Code className="h-5 w-5" />
                生成的代码
              </CardTitle>
              {codeResult && (
                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    icon={<Copy className="h-4 w-4" />}
                    onClick={handleCopy}
                  />
                  <Button
                    variant="ghost"
                    size="sm"
                    icon={<Download className="h-4 w-4" />}
                  />
                </div>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {codeResult ? (
              <div className="space-y-4">
                <div className="h-[400px] rounded-lg overflow-hidden">
                  <Editor
                    height="100%"
                    defaultLanguage={language}
                    theme="vs-dark"
                    value={codeResult.code}
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      fontSize: 14,
                    }}
                  />
                </div>

                {codeResult.explanation && (
                  <div>
                    <h4 className="font-semibold mb-2">代码说明</h4>
                    <p className="text-sm text-muted-foreground">{codeResult.explanation}</p>
                  </div>
                )}

                {codeResult.suggestions && codeResult.suggestions.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">改进建议</h4>
                    <div className="space-y-2">
                      {codeResult.suggestions.map((suggestion, idx) => (
                        <div key={idx} className="bg-muted rounded-lg p-3 text-sm">
                          {suggestion}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-[400px] text-center text-muted-foreground">
                <Code className="h-12 w-12 mb-4 opacity-50" />
                <p>输入功能描述并点击生成按钮</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
