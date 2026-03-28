import React, { useState } from 'react';
import { Play, History, Copy, Trash2 } from 'lucide-react';
import { Button } from '../../components/Button';
import { Input } from '../../components/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { useApiStore } from '../../stores/apiStore';
import { formatDateTime } from '../../utils';
import { useCopyToClipboard } from '../../hooks/useCopyToClipboard';

export const DebugTool: React.FC = () => {
  const { debugHistory, loading, sendDebugRequest, fetchDebugHistory } = useApiStore();
  const [method, setMethod] = useState('GET');
  const [url, setUrl] = useState('');
  const [headers, setHeaders] = useState('');
  const [body, setBody] = useState('');
  const [, copy] = useCopyToClipboard();

  const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];

  const handleSend = async () => {
    if (!url.trim()) return;

    const headerObj: Record<string, string> = {};
    try {
      if (headers.trim()) {
        headers.split('\n').forEach((line) => {
          const [key, value] = line.split(':').map((s) => s.trim());
          if (key && value) headerObj[key] = value;
        });
      }
    } catch (e) {
      console.error('Invalid headers format');
    }

    const bodyObj = body.trim() ? JSON.parse(body) : undefined;

    await sendDebugRequest({
      method,
      url,
      headers: headerObj,
      body: bodyObj,
    });
  };

  const handleCopy = (text: string) => {
    copy(text);
  };

  const getMethodBadge = (method: string) => {
    const colors: Record<string, 'primary' | 'success' | 'warning' | 'danger'> = {
      GET: 'success',
      POST: 'primary',
      PUT: 'warning',
      DELETE: 'danger',
      PATCH: 'primary',
    };
    return <Badge variant={colors[method] || 'default'}>{method}</Badge>;
  };

  const getStatusCodeBadge = (code?: number) => {
    if (!code) return null;
    const variant = code >= 200 && code < 300 ? 'success' : 'danger';
    return <Badge variant={variant}>{code}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">调试工具</h2>
        <p className="text-muted-foreground">测试API接口并查看响应</p>
      </div>

      {/* Request Builder */}
      <Card>
        <CardHeader>
          <CardTitle>构建请求</CardTitle>
          <CardDescription>配置API请求参数</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value)}
              className="rounded-lg border border-input bg-background px-3 py-2 font-medium"
            >
              {methods.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            <Input
              className="flex-1"
              placeholder="https://api.example.com/endpoint"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <Button onClick={handleSend} loading={loading} icon={<Play className="h-4 w-4" />}>
              发送
            </Button>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">请求头 (每行一个，格式: Key: Value)</label>
            <textarea
              className="flex min-h-[100px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
              placeholder="Content-Type: application/json&#10;Authorization: Bearer your-token"
              value={headers}
              onChange={(e) => setHeaders(e.target.value)}
            />
          </div>

          {['POST', 'PUT', 'PATCH'].includes(method) && (
            <div>
              <label className="block text-sm font-medium mb-2">请求体 (JSON)</label>
              <textarea
                className="flex min-h-[150px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm font-mono"
                placeholder='{"key": "value"}'
                value={body}
                onChange={(e) => setBody(e.target.value)}
              />
            </div>
          )}
        </CardContent>
      </Card>

      {/* History */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>调试历史</CardTitle>
              <CardDescription>最近的API请求记录</CardDescription>
            </div>
            <Button variant="ghost" size="sm" icon={<History className="h-4 w-4" />}>
              刷新
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {debugHistory.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">
              暂无调试记录
            </p>
          ) : (
            <div className="space-y-4">
              {debugHistory.map((item) => (
                <div key={item.id} className="border rounded-lg p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {getMethodBadge(item.method)}
                      <span className="text-sm font-mono">{item.url}</span>
                      {getStatusCodeBadge(item.statusCode)}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span>{item.duration}ms</span>
                      <span>{formatDateTime(item.timestamp)}</span>
                    </div>
                  </div>

                  {item.response && (
                    <div className="mt-3">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium">响应</span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCopy(JSON.stringify(item.response, null, 2))}
                          icon={<Copy className="h-4 w-4" />}
                        />
                      </div>
                      <pre className="rounded bg-muted p-3 text-sm overflow-x-auto max-h-48">
                        {JSON.stringify(item.response, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
