import React from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { SdkList } from './SdkList';
import { IntegrationGuide } from './IntegrationGuide';

export const SdkPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">SDK管理</h1>
        <p className="mt-2 text-muted-foreground">
          下载SDK、查看集成文档和版本更新
        </p>
      </div>

      <Tabs defaultValue="list">
        <TabsList>
          <TabsTrigger value="list">SDK列表</TabsTrigger>
          <TabsTrigger value="guide">集成指南</TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="mt-6">
          <SdkList />
        </TabsContent>

        <TabsContent value="guide" className="mt-6">
          <IntegrationGuide />
        </TabsContent>
      </Tabs>
    </div>
  );
};
