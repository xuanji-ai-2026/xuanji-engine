import React from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { PluginList } from './PluginList';
import { PluginEditor } from './PluginEditor';
import { PluginTesting } from './PluginTesting';
import { PluginMarketplace } from './PluginMarketplace';

export const PluginPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">插件开发</h1>
        <p className="mt-2 text-muted-foreground">
          开发、测试和发布插件，浏览插件市场
        </p>
      </div>

      <Tabs defaultValue="list">
        <TabsList>
          <TabsTrigger value="list">我的插件</TabsTrigger>
          <TabsTrigger value="editor">开发工具</TabsTrigger>
          <TabsTrigger value="testing">测试环境</TabsTrigger>
          <TabsTrigger value="marketplace">插件市场</TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="mt-6">
          <PluginList />
        </TabsContent>

        <TabsContent value="editor" className="mt-6">
          <PluginEditor />
        </TabsContent>

        <TabsContent value="testing" className="mt-6">
          <PluginTesting />
        </TabsContent>

        <TabsContent value="marketplace" className="mt-6">
          <PluginMarketplace />
        </TabsContent>
      </Tabs>
    </div>
  );
};
