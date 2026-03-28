/**
 * 小元 - API 管理服务
 * 提供接口查询、文档生成、测试协助等功能
 */

import {
  ApiEndpoint,
  ApiTestRequest,
  ApiTestResponse,
  ApiGenerationRequest,
  ApiResponse,
  CodeExample,
} from '../types';

export class ApiManagementService {
  private endpoints: Map<string, ApiEndpoint> = new Map();
  private config: any;
  private logger: any;

  constructor(config: any, logger: any) {
    this.config = config;
    this.logger = logger;
  }

  /**
   * 获取所有 API 端点
   */
  async getAllEndpoints(): Promise<ApiEndpoint[]> {
    this.logger.debug('Fetching all API endpoints');
    return Array.from(this.endpoints.values());
  }

  /**
   * 根据 ID 获取 API 端点
   */
  async getEndpointById(id: string): Promise<ApiEndpoint | null> {
    this.logger.debug(`Fetching API endpoint: ${id}`);
    return this.endpoints.get(id) || null;
  }

  /**
   * 根据 tag 搜索 API 端点
   */
  async searchByTags(tags: string[]): Promise<ApiEndpoint[]> {
    this.logger.debug(`Searching endpoints by tags: ${tags.join(', ')}`);
    return Array.from(this.endpoints.values()).filter(endpoint =>
      tags.some(tag => endpoint.tags.includes(tag))
    );
  }

  /**
   * 添加/更新 API 端点
   */
  async addEndpoint(endpoint: ApiEndpoint): Promise<void> {
    this.logger.debug(`Adding/updating endpoint: ${endpoint.id}`);
    this.endpoints.set(endpoint.id, endpoint);
  }

  /**
   * 批量导入 API 端点
   */
  async importEndpoints(endpoints: ApiEndpoint[]): Promise<number> {
    this.logger.debug(`Importing ${endpoints.length} endpoints`);
    endpoints.forEach(endpoint => this.endpoints.set(endpoint.id, endpoint));
    return endpoints.length;
  }

  /**
   * 生成 API 文档
   */
  async generateDocumentation(format: 'markdown' | 'html' | 'openapi' = 'markdown'): Promise<string> {
    this.logger.debug(`Generating API documentation in ${format} format`);

    switch (format) {
      case 'markdown':
        return this.generateMarkdownDoc();
      case 'html':
        return this.generateHtmlDoc();
      case 'openapi':
        return this.generateOpenApiSpec();
      default:
        throw new Error(`Unsupported documentation format: ${format}`);
    }
  }

  /**
   * 生成 Markdown 格式文档
   */
  private generateMarkdownDoc(): string {
    let doc = '# API 文档\n\n';
    doc += '## 概览\n';
    doc += `本文档包含 ${this.endpoints.size} 个 API 端点。\n\n`;

    // 按路径分组
    const grouped = new Map<string, ApiEndpoint[]>();
    this.endpoints.forEach(endpoint => {
      const pathBase = endpoint.path.split('/')[1] || 'root';
      if (!grouped.has(pathBase)) {
        grouped.set(pathBase, []);
      }
      grouped.get(pathBase)!.push(endpoint);
    });

    // 生成每个组的文档
    grouped.forEach((endpoints, group) => {
      doc += `## ${group}\n\n`;
      endpoints.forEach(endpoint => {
        doc += `### ${endpoint.method} ${endpoint.path}\n\n`;
        doc += `${endpoint.description}\n\n`;

        // 参数
        if (endpoint.parameters.length > 0) {
          doc += '#### 参数\n\n';
          doc += '| 参数名 | 类型 | 必需 | 描述 |\n';
          doc += '|--------|------|------|------|\n';
          endpoint.parameters.forEach(param => {
            doc += `| ${param.name} | ${param.type} | ${param.required ? '是' : '否'} | ${param.description} |\n`;
          });
          doc += '\n';
        }

        // 响应
        if (Object.keys(endpoint.responses).length > 0) {
          doc += '#### 响应\n\n';
          Object.entries(endpoint.responses).forEach(([status, schema]) => {
            doc += `**${status}**: ${schema.description || schema.type}\n\n`;
          });
        }

        doc += '---\n\n';
      });
    });

    return doc;
  }

  /**
   * 生成 HTML 格式文档
   */
  private generateHtmlDoc(): string {
    // 简化的 HTML 文档生成
    const md = this.generateMarkdownDoc();
    return `
<!DOCTYPE html>
<html>
<head>
  <title>API 文档</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
    h1, h2, h3 { color: #333; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #4CAF50; color: white; }
  </style>
</head>
<body>
  <pre>${md}</pre>
</body>
</html>`;
  }

  /**
   * 生成 OpenAPI 规范
   */
  private generateOpenApiSpec(): string {
    const openapi = {
      openapi: '3.0.0',
      info: {
        title: 'Xuanji API',
        version: '1.0.0',
        description: '玄玑引擎 API 文档',
      },
      paths: {},
    } as any;

    this.endpoints.forEach(endpoint => {
      if (!openapi.paths[endpoint.path]) {
        openapi.paths[endpoint.path] = {};
      }

      openapi.paths[endpoint.path][endpoint.method.toLowerCase()] = {
        summary: endpoint.description,
        tags: endpoint.tags,
        parameters: endpoint.parameters.map(param => ({
          name: param.name,
          in: 'query',
          required: param.required,
          schema: { type: param.type },
          description: param.description,
        })),
        responses: Object.fromEntries(
          Object.entries(endpoint.responses).map(([status, schema]) => [
            status,
            {
              description: schema.description,
              content: {
                'application/json': {
                  schema: { type: schema.type },
                },
              },
            },
          ])
        ),
      };
    });

    return JSON.stringify(openapi, null, 2);
  }

  /**
   * 执行 API 测试
   */
  async testApi(request: ApiTestRequest): Promise<ApiTestResponse> {
    this.logger.debug(`Testing API: ${request.method} ${request.url}`);

    const startTime = Date.now();

    try {
      const options: RequestInit = {
        method: request.method,
        headers: {
          'Content-Type': 'application/json',
          ...request.headers,
        },
      };

      if (request.body && ['POST', 'PUT', 'PATCH'].includes(request.method)) {
        options.body = JSON.stringify(request.body);
      }

      // 构建完整 URL
      let url = request.url;
      if (request.queryParams && Object.keys(request.queryParams).length > 0) {
        const params = new URLSearchParams(request.queryParams);
        url += `?${params.toString()}`;
      }

      const response = await fetch(url, options);
      const responseHeaders: Record<string, string> = {};
      response.headers.forEach((value, key) => {
        responseHeaders[key] = value;
      });

      let body;
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        body = await response.json();
      } else {
        body = await response.text();
      }

      return {
        success: response.ok,
        status: response.status,
        headers: responseHeaders,
        body,
        duration: Date.now() - startTime,
        timestamp: Date.now(),
      };
    } catch (error: any) {
      this.logger.error(`API test failed: ${error.message}`);
      return {
        success: false,
        status: 0,
        headers: {},
        body: { error: error.message },
        duration: Date.now() - startTime,
        timestamp: Date.now(),
      };
    }
  }

  /**
   * 生成 API 测试用例
   */
  async generateTestCases(endpointId: string): Promise<CodeExample[]> {
    const endpoint = await this.getEndpointById(endpointId);
    if (!endpoint) {
      throw new Error(`Endpoint not found: ${endpointId}`);
    }

    const examples: CodeExample[] = [];

    // cURL 示例
    examples.push({
      title: 'cURL 请求示例',
      description: '使用 cURL 进行 API 调用',
      language: 'bash',
      code: `curl -X ${endpoint.method} \\
  http://localhost:5000${endpoint.path} \\
  -H "Content-Type: application/json" \\
  -d '${JSON.stringify({ example: 'data' }, null, 2)}'`,
    });

    // JavaScript 示例
    examples.push({
      title: 'JavaScript Fetch 示例',
      description: '使用 fetch API 进行调用',
      language: 'javascript',
      code: `fetch('http://localhost:5000${endpoint.path}', {
  method: '${endpoint.method}',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ example: 'data' }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));`,
    });

    // TypeScript 示例
    examples.push({
      title: 'TypeScript Axios 示例',
      description: '使用 axios 进行类型安全调用',
      language: 'typescript',
      code: `import axios from 'axios';

interface Response {
  success: boolean;
  data: any;
}

const response = await axios<Response>({
  method: '${endpoint.method.toLowerCase()}',
  url: 'http://localhost:5000${endpoint.path}',
  data: { example: 'data' },
});

console.log(response.data);`,
    });

    return examples;
  }

  /**
   * 基于描述生成 API 端点建议
   */
  async suggestApiEndpoint(request: ApiGenerationRequest): Promise<ApiEndpoint[]> {
    this.logger.debug(`Generating API endpoint suggestions for: ${request.description}`);

    // 这里应该调用核心 AI 服务来生成建议
    // 暂时返回一个示例
    const suggestions: ApiEndpoint[] = [
      {
        id: `api_${Date.now()}`,
        path: `/api/v1/${request.endpointName || 'resource'}`,
        method: (request.method as any) || 'GET',
        description: request.description,
        tags: ['generated', 'suggestion'],
        parameters: [],
        responses: {
          200: {
            type: 'object',
            description: '成功响应',
          },
        },
        authRequired: true,
      },
    ];

    return suggestions;
  }

  /**
   * 验证 API 端点配置
   */
  async validateEndpoint(endpoint: ApiEndpoint): Promise<{ valid: boolean; errors: string[] }> {
    const errors: string[] = [];

    if (!endpoint.id) {
      errors.push('API ID 不能为空');
    }

    if (!endpoint.path) {
      errors.push('API 路径不能为空');
    }

    if (!endpoint.path.startsWith('/')) {
      errors.push('API 路径必须以 / 开头');
    }

    if (!['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].includes(endpoint.method)) {
      errors.push('无效的 HTTP 方法');
    }

    if (!endpoint.description) {
      errors.push('API 描述不能为空');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}
