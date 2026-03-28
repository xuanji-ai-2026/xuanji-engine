import React, { useEffect } from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { ApiKeys } from './ApiKeys';
import { Statistics } from './Statistics';
import { DebugTool } from './DebugTool';
import { Documentation } from './Documentation';

export const ApiPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">API管理</h1>
        <p className="mt-2 text-muted-foreground">
          管理API密钥、查看调用统计、调试接口、查看文档
        </p>
      </div>

      <Tabs defaultValue="keys">
        <TabsList>
          <TabsTrigger value="keys">密钥管理</TabsTrigger>
          <TabsTrigger value="stats">调用统计</TabsTrigger>
          <TabsTrigger value="debug">调试工具</TabsTrigger>
          <TabsTrigger value="docs">API文档</TabsTrigger>
        </TabsList>

        <TabsContent value="keys" className="mt-6">
          <ApiKeys />
        </TabsContent>

        <TabsContent value="stats" className="mt-6">
          <Statistics />
        </TabsContent>

        <TabsContent value="debug" className="mt-6">
          <DebugTool />
        </TabsContent>

        <TabsContent value="docs" className="mt-6">
          <Documentation />
        </TabsContent>
      </Tabs>
    </div>
  );
};
