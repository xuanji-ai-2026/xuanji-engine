import React, { useState } from 'react';
import { AlertTriangle, Bug, Lightbulb, CheckCircle } from 'lucide-react';
import { Button } from '../../components/Button';
import { Textarea } from '../../components/Input';
import { Input } from '../../components/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { useAssistantStore } from '../../stores/assistantStore';
import Editor from '@monaco-editor/react';

export const ErrorDiagnostics: React.FC = () => {
  const { diagnostics, loading, diagnoseError } = useAssistantStore();
  const [error, setError] = useState('');
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('typescript');

  const handleDiagnose = async () => {
    await diagnoseError(error, code || undefined, language);
  };

  const getSeverityBadge = (severity: string) => {
    const variants: Record<string, 'success' | 'warning' | 'danger'> = {
      info: 'success',
      warning: 'warning',
      error: 'danger',
    };
    return <Badge variant={variants[severity]}>{severity}</Badge>;
  };

  const getSeverityIcon = (severity: string) => {
    const icons: Record<string, any> = {
      info: <CheckCircle className="h-5 w-5 text-blue-500" />,
      warning: <AlertTriangle className="h-5 w-5 text-yellow-500" />,
      error: <Bug className="h-5 w-5 text-red-500" />,
    };
    return icons[severity] || icons.info;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">错误诊断</h2>
        <p className="text-muted-foreground">AI驱动的错误分析和修复建议</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Input Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Bug className="h-5 w-5" />
              错误信息
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">错误消息</label>
              <Textarea
                placeholder="粘贴错误消息，例如：Uncaught TypeError: Cannot read property 'foo' of undefined"
                value={error}
                onChange={(e) => setError(e.target.value)}
                rows={4}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">相关代码 (可选)</label>
              <div className="h-[200px] rounded-lg overflow-hidden">
                <Editor
                  height="100%"
                  defaultLanguage={language}
                  theme="vs-dark"
                  value={code}
                  onChange={(value) => setCode(value || '')}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 12,
                  }}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">编程语言</label>
              <Input
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                placeholder="typescript"
              />
            </div>

            <Button
              className="w-full"
              onClick={handleDiagnose}
              loading={loading}
              disabled={!error.trim()}
              icon={<AlertTriangle className="h-4 w-4" />}
            >
              诊断错误
            </Button>
          </CardContent>
        </Card>

        {/* Results Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Lightbulb className="h-5 w-5" />
              诊断结果
            </CardTitle>
          </CardHeader>
          <CardContent>
            {diagnostics.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-[400px] text-center text-muted-foreground">
                <AlertTriangle className="h-12 w-12 mb-4 opacity-50" />
                <p>输入错误信息进行诊断</p>
              </div>
            ) : (
              <div className="space-y-4 max-h-[500px] overflow-y-auto">
                {diagnostics.map((diag) => (
                  <div
                    key={diag.id}
                    className="border rounded-lg p-4 space-y-3"
                  >
                    <div className="flex items-start gap-3">
                      {getSeverityIcon(diag.severity)}
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex items-center gap-2">
                            {getSeverityBadge(diag.severity)}
                            {diag.line !== undefined && (
                              <Badge variant="outline">Line {diag.line}</Badge>
                            )}
                          </div>
                        </div>
                        <p className="font-medium">{diag.message}</p>
                      </div>
                    </div>

                    {diag.code && (
                      <div className="mt-2">
                        <pre className="bg-muted rounded p-3 text-sm overflow-x-auto">
                          {diag.code}
                        </pre>
                      </div>
                    )}

                    {diag.fixSuggestion && (
                      <div className="mt-2 bg-green-50 dark:bg-green-950 rounded-lg p-3">
                        <div className="flex items-center gap-2 text-sm font-medium text-green-700 dark:text-green-300 mb-1">
                          <Lightbulb className="h-4 w-4" />
                          修复建议
                        </div>
                        <p className="text-sm text-green-600 dark:text-green-400">
                          {diag.fixSuggestion}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
