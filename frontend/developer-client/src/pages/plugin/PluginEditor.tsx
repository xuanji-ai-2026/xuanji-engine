import React, { useEffect, useState } from 'react';
import { Save, Play, Code, Settings, FileText, FolderTree } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { Input } from '../../components/Input';
import Editor from '@monaco-editor/react';

export const PluginEditor: React.FC = () => {
  const [activeFile, setActiveFile] = useState('index.ts');
  const [code, setCode] = useState(`// 插件主入口文件
export interface PluginConfig {
  name: string;
  version: string;
}

export function init(config: PluginConfig) {
  console.log('Plugin initialized:', config.name);
}

export function execute(input: any): any {
  // 在这里实现你的插件逻辑
  return {
    success: true,
    data: input
  };
}`);

  const files = [
    { name: 'index.ts', icon: <Code className="h-4 w-4" /> },
    { name: 'package.json', icon: <FileText className="h-4 w-4" /> },
    { name: 'README.md', icon: <FileText className="h-4 w-4" /> },
    { name: 'utils.ts', icon: <Code className="h-4 w-4" /> },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">插件编辑器</h2>
          <p className="text-muted-foreground">编写和编辑插件代码</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" icon={<Play className="h-4 w-4" />}>
            运行测试
          </Button>
          <Button icon={<Save className="h-4 w-4" />}>
            保存
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* File Tree */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <FolderTree className="h-5 w-5" />
                文件
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-1">
                {files.map((file) => (
                  <button
                    key={file.name}
                    onClick={() => setActiveFile(file.name)}
                    className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg transition-colors ${
                      activeFile === file.name
                        ? 'bg-primary text-primary-foreground'
                        : 'hover:bg-muted'
                    }`}
                  >
                    {file.icon}
                    <span className="text-sm">{file.name}</span>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Editor */}
        <div className="lg:col-span-3">
          <Card className="h-[600px]">
            <CardHeader className="border-b">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Code className="h-4 w-4" />
                  <span className="font-mono text-sm">{activeFile}</span>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="sm">
                    格式化
                  </Button>
                  <Button variant="ghost" size="sm">
                    自动完成
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0 h-[calc(100%-60px)]">
              <Editor
                height="100%"
                defaultLanguage="typescript"
                theme="vs-dark"
                value={code}
                onChange={(value) => setCode(value || '')}
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                }}
              />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Config Panel */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Settings className="h-5 w-5" />
            插件配置
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm font-medium mb-2">插件名称</label>
              <Input placeholder="my-awesome-plugin" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">版本</label>
              <Input placeholder="1.0.0" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">作者</label>
              <Input placeholder="Your Name" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">描述</label>
              <Input placeholder="Plugin description" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
