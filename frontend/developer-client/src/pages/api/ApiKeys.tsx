import React, { useEffect, useState } from 'react';
import { Plus, Key, Copy, Trash2, Ban, Eye, EyeOff } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Modal } from '../../components/Modal';
import { Input } from '../../components/Input';
import { Badge } from '../../components/Badge';
import { useApiStore } from '../../stores/apiStore';
import { formatDateTime } from '../../utils';
import { useCopyToClipboard } from '../../hooks/useCopyToClipboard';

export const ApiKeys: React.FC = () => {
  const { apiKeys, loading, fetchApiKeys, createApiKey, deleteApiKey, revokeApiKey } = useApiStore();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showKey, setShowKey] = useState<Record<string, boolean>>({});
  const [name, setName] = useState('');
  const [, copy] = useCopyToClipboard();

  useEffect(() => {
    fetchApiKeys();
  }, [fetchApiKeys]);

  const handleCreate = async () => {
    if (!name.trim()) return;
    await createApiKey({ name, permissions: ['read', 'write'] });
    setName('');
    setShowCreateModal(false);
  };

  const handleCopy = (key: string) => {
    copy(key);
  };

  const toggleKeyVisibility = (id: string) => {
    setShowKey((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const maskKey = (key: string) => {
    return key.slice(0, 8) + '...' + key.slice(-4);
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, 'success' | 'warning' | 'danger'> = {
      active: 'success',
      revoked: 'danger',
      expired: 'warning',
    };
    return <Badge variant={variants[status] || 'default'}>{status}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">API密钥</h2>
          <p className="text-muted-foreground">管理您的API访问密钥</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)} icon={<Plus className="h-4 w-4" />}>
          创建密钥
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {apiKeys.map((key) => (
          <Card key={key.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <Key className="h-5 w-5 text-primary" />
                  <CardTitle className="text-lg">{key.name}</CardTitle>
                </div>
                {getStatusBadge(key.status)}
              </div>
              <CardDescription>
                创建于 {formatDateTime(key.createdAt)}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <code className="flex-1 rounded bg-muted px-2 py-1 text-sm">
                    {showKey[key.id] ? key.key : maskKey(key.key)}
                  </code>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => toggleKeyVisibility(key.id)}
                    icon={showKey[key.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  />
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleCopy(key.key)}
                    icon={<Copy className="h-4 w-4" />}
                  />
                </div>

                {key.lastUsedAt && (
                  <p className="text-xs text-muted-foreground">
                    最后使用: {formatDateTime(key.lastUsedAt)}
                  </p>
                )}

                <div className="flex gap-2">
                  {key.status === 'active' && (
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => revokeApiKey(key.id)}
                      icon={<Ban className="h-4 w-4" />}
                    >
                      撤销
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => deleteApiKey(key.id)}
                    icon={<Trash2 className="h-4 w-4" />}
                  >
                    删除
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}

        {apiKeys.length === 0 && !loading && (
          <Card className="col-span-full">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Key className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">暂无API密钥</p>
              <Button onClick={() => setShowCreateModal(true)} className="mt-4">
                创建第一个密钥
              </Button>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Create Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="创建API密钥"
        footer={
          <>
            <Button variant="outline" onClick={() => setShowCreateModal(false)}>
              取消
            </Button>
            <Button onClick={handleCreate} loading={loading}>
              创建
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">密钥名称</label>
            <Input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="输入密钥名称"
            />
          </div>
          <p className="text-sm text-muted-foreground">
            创建后，密钥将只显示一次，请妥善保存。
          </p>
        </div>
      </Modal>
    </div>
  );
};
