import React from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { Chat } from './Chat';
import { CodeGenerator } from './CodeGenerator';
import { ErrorDiagnostics } from './ErrorDiagnostics';
import { OptimizationSuggestions } from './OptimizationSuggestions';

export const AssistantPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">智能助手小元</h1>
        <p className="mt-2 text-muted-foreground">
          AI驱动的开发助手：代码生成、错误诊断、优化建议
        </p>
      </div>

      <Tabs defaultValue="chat">
        <TabsList>
          <TabsTrigger value="chat">对话助手</TabsTrigger>
          <TabsTrigger value="code">代码生成</TabsTrigger>
          <TabsTrigger value="diagnostics">错误诊断</TabsTrigger>
          <TabsTrigger value="optimization">优化建议</TabsTrigger>
        </TabsList>

        <TabsContent value="chat" className="mt-6">
          <Chat />
        </TabsContent>

        <TabsContent value="code" className="mt-6">
          <CodeGenerator />
        </TabsContent>

        <TabsContent value="diagnostics" className="mt-6">
          <ErrorDiagnostics />
        </TabsContent>

        <TabsContent value="optimization" className="mt-6">
          <OptimizationSuggestions />
        </TabsContent>
      </Tabs>
    </div>
  );
};
