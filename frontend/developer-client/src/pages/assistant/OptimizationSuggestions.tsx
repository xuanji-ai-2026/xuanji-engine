import React, { useState } from 'react';
import { Zap, Rocket, Shield, Wrench, TrendingUp } from 'lucide-react';
import { Button } from '../../components/Button';
import { Textarea } from '../../components/Input';
import { Input } from '../../components/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { useAssistantStore } from '../../stores/assistantStore';
import Editor from '@monaco-editor/react';

export const OptimizationSuggestions: React.FC = () => {
  const { optimizations, loading, getOptimizations } = useAssistantStore();
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('typescript');

  const handleOptimize = async () => {
    await getOptimizations(code, language);
  };

  const getTypeIcon = (type: string) => {
    const icons: Record<string, any> = {
      performance: <Rocket className="h-5 w-5 text-blue-500" />,
      security: <Shield className="h-5 w-5 text-green-500" />,
      maintainability: <Wrench className="h-5 w-5 text-orange-500" />,
      'best-practice': <TrendingUp className="h-5 w-5 text-purple-500" />,
    };
    return icons[type] || <Zap className="h-5 w-5" />;
  };

  const getTypeBadge = (type: string) => {
    const colors: Record<string, string> = {
      performance: 'bg-blue-100 text-blue-800',
      security: 'bg-green-100 text-green-800',
      maintainability: 'bg-orange-100 text-orange-800',
      'best-practice': 'bg-purple-100 text-purple-800',
    };
    return (
      <Badge className={colors[type] || ''}>{type}</Badge>
    );
  };

  const getImpactBadge = (impact: string) => {
    const variants: Record<string, 'success' | 'warning' | 'danger'> = {
      high: 'danger',
      medium: 'warning',
      low: 'success',
    };
    return <Badge variant={variants[impact]}>{impact}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">优化建议</h2>
        <p className="text-muted-foreground">AI分析代码并提供优化建议</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Input Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Zap className="h-5 w-5" />
              代码输入
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">代码</label>
              <div className="h-[400px] rounded-lg overflow-hidden">
                <Editor
                  height="100%"
                  defaultLanguage={language}
                  theme="vs-dark"
                  value={code}
                  onChange={(value) => setCode(value || '')}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
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
              onClick={handleOptimize}
              loading={loading}
              disabled={!code.trim()}
              icon={<Zap className="h-4 w-4" />}
            >
              分析优化
            </Button>
          </CardContent>
        </Card>

        {/* Results Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              优化建议
            </CardTitle>
          </CardHeader>
          <CardContent>
            {optimizations.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-[400px] text-center text-muted-foreground">
                <Zap className="h-12 w-12 mb-4 opacity-50" />
                <p>输入代码进行分析</p>
              </div>
            ) : (
              <Tabs defaultValue="list">
                <TabsList>
                  <TabsTrigger value="list">列表视图</TabsTrigger>
                  <TabsTrigger value="compare">代码对比</TabsTrigger>
                </TabsList>

                <TabsContent value="list" className="mt-4">
                  <div className="space-y-3 max-h-[500px] overflow-y-auto">
                    {optimizations.map((opt) => (
                      <div
                        key={opt.id}
                        className="border rounded-lg p-4 space-y-2"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-2">
                            {getTypeIcon(opt.type)}
                            <div>
                              <div className="font-medium">{opt.title}</div>
                              <div className="flex gap-2 mt-1">
                                {getTypeBadge(opt.type)}
                                {getImpactBadge(opt.impact)}
                              </div>
                            </div>
                          </div>
                        </div>

                        <p className="text-sm text-muted-foreground">
                          {opt.description}
                        </p>

                        <div className="text-xs text-muted-foreground mt-2">
                          点击"代码对比"查看详细改进
                        </div>
                      </div>
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="compare" className="mt-4">
                  <div className="space-y-4 max-h-[500px] overflow-y-auto">
                    {optimizations.map((opt) => (
                      <div key={opt.id} className="border rounded-lg overflow-hidden">
                        <div className="bg-muted px-4 py-2 flex items-center gap-2">
                          {getTypeIcon(opt.type)}
                          <span className="font-medium">{opt.title}</span>
                        </div>
                        <div className="grid grid-cols-2">
                          <div>
                            <div className="bg-red-50 dark:bg-red-950 px-4 py-2 text-sm font-medium text-red-700 dark:text-red-300">
                              原代码
                            </div>
                            <pre className="p-4 text-sm overflow-x-auto bg-red-950/10">
                              {opt.code}
                            </pre>
                          </div>
                          <div>
                            <div className="bg-green-50 dark:bg-green-950 px-4 py-2 text-sm font-medium text-green-700 dark:text-green-300">
                              优化后
                            </div>
                            <pre className="p-4 text-sm overflow-x-auto bg-green-950/10">
                              {opt.improvedCode}
                            </pre>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </TabsContent>
              </Tabs>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
