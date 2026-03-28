import React, { useEffect } from 'react';
import { Download, Book, Clock, Package, FileText } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { useSdkStore } from '../../stores/sdkStore';
import { formatBytes, formatDate } from '../../utils';

export const SdkList: React.FC = () => {
  const { sdks, loading, fetchSdks, downloadSdk } = useSdkStore();

  useEffect(() => {
    fetchSdks();
  }, [fetchSdks]);

  const platformIcons: Record<string, any> = {
    javascript: '⚡',
    python: '🐍',
    java: '☕',
    go: '🐹',
    rust: '🦀',
    php: '🐘',
    csharp: '💜',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">SDK列表</h2>
          <p className="text-muted-foreground">下载各平台的官方SDK</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {sdks.map((sdk) => (
          <Card key={sdk.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{platformIcons[sdk.platform]}</span>
                  <div>
                    <CardTitle className="text-xl">{sdk.name}</CardTitle>
                    <CardDescription className="mt-1">{sdk.description}</CardDescription>
                  </div>
                </div>
                <Badge variant="outline">v{sdk.version}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Package className="h-4 w-4 text-muted-foreground" />
                    <span>大小: {formatBytes(sdk.size)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span>发布: {formatDate(sdk.releasedAt)}</span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button
                    className="flex-1"
                    onClick={() => downloadSdk(sdk.id)}
                    loading={loading}
                    icon={<Download className="h-4 w-4" />}
                  >
                    下载SDK
                  </Button>
                  <Button
                    variant="outline"
                    icon={<Book className="h-4 w-4" />}
                  >
                    文档
                  </Button>
                  <Button
                    variant="outline"
                    icon={<FileText className="h-4 w-4" />}
                  >
                    更新日志
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
