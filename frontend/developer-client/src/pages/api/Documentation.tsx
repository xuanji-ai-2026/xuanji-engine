import React, { useEffect, useState } from 'react';
import { Search, Code, Download, Book } from 'lucide-react';
import { Button } from '../../components/Button';
import { Input } from '../../components/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Badge } from '../../components/Badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/Tabs';
import { useApiStore } from '../../stores/apiStore';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export const Documentation: React.FC = () => {
  const { documents, currentDocument, loading, fetchDocuments, fetchDocument } = useApiStore();
  const [search, setSearch] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('javascript');

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const filteredDocuments = documents.filter((doc) =>
    doc.name.toLowerCase().includes(search.toLowerCase())
  );

  const languages = ['javascript', 'python', 'java', 'curl'];

  if (!currentDocument && filteredDocuments.length > 0) {
    fetchDocument(filteredDocuments[0].id);
  }

  const getMethodBadge = (method: string) => {
    const colors: Record<string, 'success' | 'primary' | 'warning' | 'danger'> = {
      GET: 'success',
      POST: 'primary',
      PUT: 'warning',
      DELETE: 'danger',
      PATCH: 'primary',
    };
    return <Badge variant={colors[method] || 'default'}>{method}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">API文档</h2>
        <p className="text-muted-foreground">查看API接口文档和使用示例</p>
      </div>

      {/* Search */}
      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            className="pl-10"
            placeholder="搜索API文档..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-2">
          <h3 className="text-sm font-semibold mb-3">文档列表</h3>
          {filteredDocuments.map((doc) => (
            <button
              key={doc.id}
              onClick={() => fetchDocument(doc.id)}
              className={`w-full text-left rounded-lg p-3 transition-colors ${
                currentDocument?.id === doc.id
                  ? 'bg-primary text-primary-foreground'
                  : 'hover:bg-muted'
              }`}
            >
              <div className="font-medium">{doc.name}</div>
              <div className="text-sm opacity-75">{doc.version}</div>
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          {currentDocument ? (
            <div className="space-y-6">
              {/* Header */}
              <Card>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-2xl">{currentDocument.name}</CardTitle>
                      <CardDescription className="mt-2">
                        {currentDocument.description}
                      </CardDescription>
                    </div>
                    <Badge variant="outline">v{currentDocument.version}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="endpoints">
                    <TabsList>
                      <TabsTrigger value="endpoints">接口列表</TabsTrigger>
                      <TabsTrigger value="examples">示例代码</TabsTrigger>
                    </TabsList>

                    <TabsContent value="endpoints" className="mt-4 space-y-4">
                      {currentDocument.endpoints.map((endpoint) => (
                        <Card key={endpoint.id}>
                          <CardHeader>
                            <div className="flex items-center gap-3">
                              {getMethodBadge(endpoint.method)}
                              <code className="text-lg font-mono">{endpoint.path}</code>
                            </div>
                            <CardDescription>{endpoint.description}</CardDescription>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            {endpoint.parameters.length > 0 && (
                              <div>
                                <h4 className="font-semibold mb-2">参数</h4>
                                <div className="rounded-lg border overflow-hidden">
                                  <table className="w-full text-sm">
                                    <thead className="bg-muted">
                                      <tr>
                                        <th className="px-4 py-2 text-left">参数名</th>
                                        <th className="px-4 py-2 text-left">类型</th>
                                        <th className="px-4 py-2 text-left">必填</th>
                                        <th className="px-4 py-2 text-left">说明</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      {endpoint.parameters.map((param) => (
                                        <tr key={param.name} className="border-t">
                                          <td className="px-4 py-2 font-mono">{param.name}</td>
                                          <td className="px-4 py-2">
                                            <Badge variant="outline">{param.type}</Badge>
                                          </td>
                                          <td className="px-4 py-2">
                                            {param.required ? '是' : '否'}
                                          </td>
                                          <td className="px-4 py-2 text-muted-foreground">
                                            {param.description}
                                          </td>
                                        </tr>
                                      ))}
                                    </tbody>
                                  </table>
                                </div>
                              </div>
                            )}

                            {endpoint.responses.length > 0 && (
                              <div>
                                <h4 className="font-semibold mb-2">响应</h4>
                                {endpoint.responses.map((response) => (
                                  <div key={response.statusCode} className="mb-3">
                                    <div className="flex items-center gap-2 mb-2">
                                      <Badge
                                        variant={response.statusCode < 300 ? 'success' : 'danger'}
                                      >
                                        {response.statusCode}
                                      </Badge>
                                      <span className="text-sm">{response.description}</span>
                                    </div>
                                    <pre className="rounded bg-muted p-3 text-sm overflow-x-auto">
                                      {JSON.stringify(response.schema, null, 2)}
                                    </pre>
                                  </div>
                                ))}
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </TabsContent>

                    <TabsContent value="examples" className="mt-4">
                      <div className="space-y-4">
                        <div className="flex gap-2 mb-4">
                          {languages.map((lang) => (
                            <Button
                              key={lang}
                              variant={selectedLanguage === lang ? 'primary' : 'outline'}
                              size="sm"
                              onClick={() => setSelectedLanguage(lang)}
                            >
                              {lang}
                            </Button>
                          ))}
                        </div>

                        {currentDocument.examples
                          .filter((ex) => ex.language === selectedLanguage)
                          .map((example, idx) => (
                            <Card key={idx}>
                              <CardHeader>
                                <div className="flex items-center justify-between">
                                  <CardTitle className="text-lg">示例 {idx + 1}</CardTitle>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    icon={<Copy className="h-4 w-4" />}
                                  />
                                </div>
                              </CardHeader>
                              <CardContent>
                                <SyntaxHighlighter
                                  language={selectedLanguage}
                                  style={vscDarkPlus}
                                  customStyle={{ borderRadius: '8px' }}
                                >
                                  {example.code}
                                </SyntaxHighlighter>
                              </CardContent>
                            </Card>
                          ))}
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Book className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">选择一个文档查看详情</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
