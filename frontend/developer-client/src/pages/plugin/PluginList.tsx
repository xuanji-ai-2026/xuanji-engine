import React, { useEffect, useState } from 'react';
import { Plus, Upload, Send, Trash2, Edit, Play } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Modal } from '../../components/Modal';
import { Input } from '../../components/Input';
import { Textarea } from '../../components/Input';
import { usePluginStore } from '../../stores/pluginStore';
import { formatDateTime } from '../../utils';

export const PluginList: React.FC = () => {
  const { plugins, loading, fetchPlugins, createPlugin, deletePlugin, submitForReview } = usePluginStore();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '', category: '', tags: '' });

  useEffect(() => {
    fetchPlugins();
  }, [fetchPlugins]);

  const handleCreate = async () => {
    await createPlugin({
      ...formData,
      tags: formData.tags.split(',').map((t) => t.trim()).filter(Boolean),
    });
    setShowCreateModal(false);
    setFormData({ name: '', description: '', category: '', tags: '' });
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, 'primary' | 'success' | 'warning' | 'danger'> = {
      draft: 'primary',
      submitted: 'warning',
      approved: 'success',
      rejected: 'danger',
      published: 'success',
    };
    return <Badge variant={variants[status] || 'default'}>{status}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">我的插件</h2>
          <p className="text-muted-foreground">管理您开发的插件</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)} icon={<Plus className="h-4 w-4" />}>
          创建插件
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {plugins.map((plugin) => (
          <Card key={plugin.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{plugin.name}</CardTitle>
                  <CardDescription className="mt-1">{plugin.description}</CardDescription>
                </div>
                {getStatusBadge(plugin.status)}
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">版本</span>
                  <Badge variant="outline">{plugin.version}</Badge>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">分类</span>
                  <span>{plugin.category}</span>
                </div>

                {plugin.downloads !== undefined && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">下载</span>
                    <span>{plugin.downloads}</span>
                  </div>
                )}

                {plugin.rating !== undefined && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">评分</span>
                    <span>⭐ {plugin.rating.toFixed(1)}</span>
                  </div>
                )}

                <div className="flex gap-2 pt-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    icon={<Edit className="h-4 w-4" />}
                  >
                    编辑
                  </Button>
                  {plugin.status === 'draft' && (
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => submitForReview(plugin.id)}
                      icon={<Send className="h-4 w-4" />}
                    >
                      提交审核
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => deletePlugin(plugin.id)}
                    icon={<Trash2 className="h-4 w-4" />}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Create Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="创建新插件"
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
            <label className="block text-sm font-medium mb-2">插件名称</label>
            <Input
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="输入插件名称"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">描述</label>
            <Textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="描述插件的功能和用途"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">分类</label>
            <Input
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              placeholder="例如: 数据处理, UI组件, 工具类"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">标签 (逗号分隔)</label>
            <Input
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              placeholder="例如: ai, nlp, text-analysis"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};
