import React, { useState } from 'react';
import { Play, RefreshCw, Bug, FileText, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';

export const PluginTesting: React.FC = () => {
  const [testing, setTesting] = useState(false);
  const [selectedPlugin, setSelectedPlugin] = useState('my-plugin');

  const testResults = [
    {
      id: '1',
      name: '初始化测试',
      passed: true,
      duration: 45,
      message: '插件初始化成功'
    },
    {
      id: '2',
      name: '功能测试 - 基础执行',
      passed: true,
      duration: 120,
      message: 'execute函数返回正确结果'
    },
    {
      id: '3',
      name: '边界条件测试',
      passed: false,
      duration: 85,
      message: '空输入处理失败'
    },
    {
      id: '4',
      name: '性能测试',
      passed: true,
      duration: 350,
      message: '响应时间在可接受范围内'
    },
  ];

  const logEntries = [
    { time: '14:23:01', level: 'info', message: '开始测试 my-plugin' },
    { time: '14:23:02', level: 'info', message: '加载插件配置...' },
    { time: '14:23:05', level: 'success', message: '初始化测试通过' },
    { time: '14:23:08', level: 'error', message: '边界条件测试失败: 无法处理空输入' },
  ];

  const runTest = async (type: string) => {
    setTesting(true);
    // 模拟测试
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setTesting(false);
  };

  const getLevelBadge = (level: string) => {
    const variants: Record<string, 'success' | 'warning' | 'danger' | 'default'> = {
      info: 'default',
      success: 'success',
      warning: 'warning',
      error: 'danger',
    };
    return <Badge variant={variants[level]}>{level}</Badge>;
  };

  const passed = testResults.filter((r) => r.passed).length;
  const failed = testResults.filter((r) => !r.passed).length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">测试环境</h2>
          <p className="text-muted-foreground">运行单元测试、集成测试和性能测试</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" icon={<RefreshCw className="h-4 w-4" />}>
            刷新
          </Button>
          <Button onClick={() => runTest('all')} loading={testing} icon={<Play className="h-4 w-4" />}>
            运行全部测试
          </Button>
        </div>
      </div>

      {/* Test Summary */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-3">
            <CardDescription>总测试数</CardDescription>
            <CardTitle className="text-3xl">{testResults.length}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>通过</CardDescription>
            <CardTitle className="text-3xl text-green-600">{passed}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>失败</CardDescription>
            <CardTitle className="text-3xl text-red-600">{failed}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>总耗时</CardDescription>
            <CardTitle className="text-3xl">
              {testResults.reduce((sum, r) => sum + r.duration, 0)}ms
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      <Tabs defaultValue="results">
        <TabsList>
          <TabsTrigger value="results">测试结果</TabsTrigger>
          <TabsTrigger value="logs">运行日志</TabsTrigger>
          <TabsTrigger value="coverage">代码覆盖率</TabsTrigger>
        </TabsList>

        <TabsContent value="results" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>测试用例结果</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {testResults.map((result) => (
                  <div
                    key={result.id}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="flex items-center gap-3">
                      {result.passed ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600" />
                      )}
                      <div>
                        <div className="font-medium">{result.name}</div>
                        <div className="text-sm text-muted-foreground">{result.message}</div>
                      </div>
                    </div>
                    <Badge variant="outline">{result.duration}ms</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logs" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>运行日志</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="font-mono text-sm space-y-2 max-h-96 overflow-y-auto">
                {logEntries.map((entry, idx) => (
                  <div key={idx} className="flex gap-3">
                    <span className="text-muted-foreground">[{entry.time}]</span>
                    {getLevelBadge(entry.level)}
                    <span>{entry.message}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="coverage" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>代码覆盖率</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium">总体覆盖率</span>
                    <span className="text-sm">75%</span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-green-500" style={{ width: '75%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium">语句覆盖率</span>
                    <span className="text-sm">82%</span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500" style={{ width: '82%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium">分支覆盖率</span>
                    <span className="text-sm">68%</span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-yellow-500" style={{ width: '68%' }}></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};
