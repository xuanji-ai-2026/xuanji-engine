import React, { useState } from 'react';
import { Search, Download, Star, TrendingUp, Clock } from 'lucide-react';
import { Button } from '../../components/Button';
import { Input } from '../../components/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';

export const PluginMarketplace: React.FC = () => {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');

  const categories = [
    { value: 'all', label: '全部' },
    { value: 'ai', label: 'AI/ML' },
    { value: 'data', label: '数据处理' },
    { value: 'ui', label: 'UI组件' },
    { value: 'tool', label: '工具类' },
    { value: 'integration', label: '集成' },
  ];

  const plugins = [
    {
      id: '1',
      name: 'GPT-4 集成插件',
      description: '集成OpenAI GPT-4模型，提供强大的文本生成和对话能力',
      author: 'Xuanji Team',
      version: '2.1.0',
      downloads: 12500,
      rating: 4.8,
      category: 'ai',
      tags: ['openai', 'gpt', 'llm'],
      price: 0,
    },
    {
      id: '2',
      name: '数据清洗工具',
      description: '自动清洗和标准化数据，支持多种格式和自定义规则',
      author: 'DataDev',
      version: '1.5.2',
      downloads: 8900,
      rating: 4.6,
      category: 'data',
      tags: ['etl', 'cleaning', 'transform'],
      price: 0,
    },
    {
      id: '3',
      name: 'UI 组件库',
      description: '美观且可定制的React组件集合',
      author: 'DesignTeam',
      version: '3.0.1',
      downloads: 15600,
      rating: 4.9,
      category: 'ui',
      tags: ['react', 'components', 'design'],
      price: 0,
    },
    {
      id: '4',
      name: '图像识别插件',
      description: '基于深度学习的图像分类和目标检测',
      author: 'VisionLab',
      version: '1.2.0',
      downloads: 6700,
      rating: 4.7,
      category: 'ai',
      tags: ['vision', 'cnn', 'detection'],
      price: 0,
    },
  ];

  const filteredPlugins = plugins.filter((p) => {
    const matchSearch = p.name.toLowerCase().includes(search.toLowerCase()) ||
                       p.description.toLowerCase().includes(search.toLowerCase());
    const matchCategory = category === 'all' || p.category === category;
    return matchSearch && matchCategory;
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">插件市场</h2>
        <p className="text-muted-foreground">浏览和安装社区插件</p>
      </div>

      {/* Search and Filter */}
      <div className="flex flex-col gap-4 md:flex-row">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            className="pl-10"
            placeholder="搜索插件..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex gap-2">
          {categories.map((cat) => (
            <Button
              key={cat.value}
              variant={category === cat.value ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setCategory(cat.value)}
            >
              {cat.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <TrendingUp className="h-5 w-5 text-primary" />
              </div>
              <div>
                <div className="text-2xl font-bold">156</div>
                <div className="text-sm text-muted-foreground">可用插件</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-green-100 flex items-center justify-center">
                <Download className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">1.2M</div>
                <div className="text-sm text-muted-foreground">总下载量</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-yellow-100 flex items-center justify-center">
                <Star className="h-5 w-5 text-yellow-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">4.7</div>
                <div className="text-sm text-muted-foreground">平均评分</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Plugin List */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredPlugins.map((plugin) => (
          <Card key={plugin.id} hover>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{plugin.name}</CardTitle>
                  <CardDescription className="mt-1">{plugin.description}</CardDescription>
                </div>
                <Badge variant="outline">v{plugin.version}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-1">
                  {plugin.tags.map((tag) => (
                    <Badge key={tag} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span>{plugin.rating.toFixed(1)}</span>
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <Download className="h-4 w-4" />
                    <span>{plugin.downloads.toLocaleString()}</span>
                  </div>
                </div>

                <div className="text-sm text-muted-foreground">
                  作者: {plugin.author}
                </div>

                <Button className="w-full" icon={<Download className="h-4 w-4" />}>
                  安装插件
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
