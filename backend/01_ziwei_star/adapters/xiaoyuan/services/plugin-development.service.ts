/**
 * 小元 - 插件开发服务
 * 提供插件模板、API 对接指导、测试建议等功能
 */

import {
  PluginTemplate,
  PluginApiGuide,
  PluginFile,
  CodeExample,
  ApiResponse,
} from '../types';

export class PluginDevelopmentService {
  private templates: Map<string, PluginTemplate> = new Map();
  private config: any;
  private logger: any;

  constructor(config: any, logger: any) {
    this.config = config;
    this.logger = logger;
    this.initializeTemplates();
  }

  /**
   * 初始化插件模板
   */
  private initializeTemplates(): void {
    // TypeScript 基础插件模板
    this.registerTemplate({
      id: 'typescript-basic-plugin',
      name: 'TypeScript 基础插件',
      description: '一个简单的 TypeScript 插件模板',
      category: 'general',
      type: 'service',
      language: 'typescript',
      files: [
        {
          path: 'src/index.ts',
          content: `/**
 * 插件入口文件
 */

import { PluginContext, PluginConfig } from './types';

export class Plugin {
  private config: PluginConfig;
  private context: PluginContext;

  constructor(config: PluginConfig) {
    this.config = config;
    this.context = {
      logger: console,
      state: {},
    };
  }

  /**
   * 插件初始化
   */
  async initialize(): Promise<void> {
    console.log('Plugin initialized');
  }

  /**
   * 插件启动
   */
  async start(): Promise<void> {
    console.log('Plugin started');
  }

  /**
   * 插件停止
   */
  async stop(): Promise<void> {
    console.log('Plugin stopped');
  }

  /**
   * 处理消息
   */
  async handle(data: any): Promise<any> {
    // 实现你的逻辑
    return { success: true, data };
  }
}

export default Plugin;`,
          isEntry: true,
          description: '插件主类',
        },
        {
          path: 'src/types.ts',
          content: `/**
 * 插件类型定义
 */

export interface PluginConfig {
  id: string;
  name: string;
  version: string;
  settings?: Record<string, any>;
}

export interface PluginContext {
  logger: any;
  state: Record<string, any>;
  api?: PluginApi;
}

export interface PluginApi {
  // 定义插件可用的 API 方法
}`,
          description: '插件类型定义',
        },
        {
          path: 'package.json',
          content: `{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Your plugin description",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}`,
          description: '项目配置',
        },
        {
          path: 'tsconfig.json',
          content: `{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "declaration": true,
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}`,
          description: 'TypeScript 配置',
        },
      ],
      dependencies: {},
      config: {
        id: 'your-plugin-id',
        name: 'Your Plugin',
        version: '1.0.0',
        permissions: ['read', 'write'],
        settings: [],
      },
    });

    // TypeScript API 插件模板
    this.registerTemplate({
      id: 'typescript-api-plugin',
      name: 'TypeScript API 插件',
      description: '基于 REST API 的插件模板',
      category: 'api',
      type: 'api',
      language: 'typescript',
      files: [
        {
          path: 'src/index.ts',
          content: `/**
 * API 插件入口文件
 */

import { PluginContext, PluginConfig } from './types';

export class ApiPlugin {
  private config: PluginConfig;
  private context: PluginContext;
  private baseUrl: string;

  constructor(config: PluginConfig) {
    this.config = config;
    this.baseUrl = config.settings?.baseUrl || '';
    this.context = {
      logger: console,
      state: {},
    };
  }

  async initialize(): Promise<void> {
    console.log('API Plugin initialized');
  }

  /**
   * 执行 API 请求
   */
  async request(endpoint: string, options?: RequestInit): Promise<any> {
    const url = \`\${this.baseUrl}\${endpoint}\`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    return response.json();
  }

  /**
   * GET 请求
   */
  async get(endpoint: string): Promise<any> {
    return this.request(endpoint, { method: 'GET' });
  }

  /**
   * POST 请求
   */
  async post(endpoint: string, data: any): Promise<any> {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default ApiPlugin;`,
          isEntry: true,
          description: 'API 插件主类',
        },
        {
          path: 'src/types.ts',
          content: `export interface PluginConfig {
  id: string;
  name: string;
  version: string;
  settings?: {
    baseUrl?: string;
    apiKey?: string;
  };
}

export interface PluginContext {
  logger: any;
  state: Record<string, any>;
}`,
          description: '类型定义',
        },
      ],
      dependencies: {},
      config: {
        id: 'api-plugin-id',
        name: 'API Plugin',
        version: '1.0.0',
        permissions: ['network', 'read'],
        settings: [
          {
            key: 'baseUrl',
            type: 'string',
            label: 'Base URL',
            required: true,
          },
          {
            key: 'apiKey',
            type: 'string',
            label: 'API Key',
          },
        ],
      },
    });
  }

  /**
   * 注册插件模板
   */
  private registerTemplate(template: PluginTemplate): void {
    this.templates.set(template.id, template);
    this.logger.debug(`Registered plugin template: ${template.id}`);
  }

  /**
   * 获取所有可用模板
   */
  async getAllTemplates(): Promise<PluginTemplate[]> {
    return Array.from(this.templates.values());
  }

  /**
   * 根据 ID 获取模板
   */
  async getTemplateById(id: string): Promise<PluginTemplate | null> {
    return this.templates.get(id) || null;
  }

  /**
   * 根据语言和类型筛选模板
   */
  async searchTemplates(language?: string, type?: string): Promise<PluginTemplate[]> {
    let templates = Array.from(this.templates.values());

    if (language) {
      templates = templates.filter(t => t.language === language);
    }

    if (type) {
      templates = templates.filter(t => t.type === type);
    }

    return templates;
  }

  /**
   * 创建插件项目文件
   */
  async createPlugin(templateId: string, pluginName: string, options?: Record<string, any>): Promise<PluginFile[]> {
    const template = await this.getTemplateById(templateId);
    if (!template) {
      throw new Error(`Template not found: ${templateId}`);
    }

    // 克隆模板文件
    const files = template.files.map(file => ({
      ...file,
      content: this.processTemplateContent(file.content, pluginName, options),
    }));

    return files;
  }

  /**
   * 处理模板内容替换
   */
  private processTemplateContent(content: string, pluginName: string, options?: Record<string, any>): string {
    let processed = content;

    // 替换插件名称
    processed = processed.replace(/your-plugin-name/g, this.kebabCase(pluginName));
    processed = processed.replace(/Your Plugin/g, pluginName);
    processed = processed.replace(/your-plugin-id/g, this.kebabCase(pluginName));

    // 替换自定义选项
    if (options) {
      Object.entries(options).forEach(([key, value]) => {
        processed = processed.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), String(value));
      });
    }

    return processed;
  }

  /**
   * 转换为 kebab-case
   */
  private kebabCase(str: string): string {
    return str
      .replace(/([a-z])([A-Z])/g, '$1-$2')
      .replace(/[\s_]+/g, '-')
      .toLowerCase();
  }

  /**
   * 生成插件 API 对接指南
   */
  async generateApiGuide(pluginId: string, apiEndpoints: any[]): Promise<PluginApiGuide> {
    this.logger.debug(`Generating API guide for plugin: ${pluginId}`);

    const guide: PluginApiGuide = {
      pluginId,
      apiEndpoints: apiEndpoints,
      usageExamples: await this.generateUsageExamples(apiEndpoints),
      integrationSteps: [
        {
          step: 1,
          title: '安装插件',
          description: '将插件文件添加到项目目录',
        },
        {
          step: 2,
          title: '配置插件',
          description: '在配置文件中设置插件参数',
          code: `const pluginConfig = {
  id: '${pluginId}',
  name: 'Your Plugin',
  version: '1.0.0',
  settings: {
    baseUrl: 'https://api.example.com',
    apiKey: 'your-api-key'
  }
};`,
        },
        {
          step: 3,
          title: '初始化插件',
          description: '在应用启动时初始化插件',
          code: `import Plugin from './your-plugin';

const plugin = new Plugin(pluginConfig);
await plugin.initialize();`,
        },
        {
          step: 4,
          title: '使用插件',
          description: '在代码中调用插件功能',
          code: `const result = await plugin.handle({ action: 'getData' });`,
        },
      ],
      testingGuide: {
        unitTests: [
          {
            title: '基本单元测试',
            description: '测试插件的基本功能',
            language: 'typescript',
            code: `import { Plugin } from '../src/index';

describe('Plugin', () => {
  let plugin: Plugin;

  beforeEach(() => {
    plugin = new Plugin({
      id: 'test-plugin',
      name: 'Test Plugin',
      version: '1.0.0',
    });
  });

  test('should initialize successfully', async () => {
    await expect(plugin.initialize()).resolves.not.toThrow();
  });

  test('should handle data correctly', async () => {
    await plugin.initialize();
    const result = await plugin.handle({ test: 'data' });
    expect(result.success).toBe(true);
  });
});`,
          },
        ],
        integrationTests: [
          {
            title: '集成测试示例',
            description: '测试插件与 API 的集成',
            language: 'typescript',
            code: `describe('Plugin Integration', () => {
  test('should communicate with API', async () => {
    const plugin = new Plugin(config);
    await plugin.initialize();
    
    const result = await plugin.get('/api/test');
    expect(result).toBeDefined();
  });
});`,
          },
        ],
        manualTests: [
          {
            title: '手动测试流程',
            description: '手动测试插件功能的步骤',
            steps: [
              '启动应用程序',
              '打开插件管理界面',
              '配置插件参数',
              '测试主要功能',
              '检查日志输出',
            ],
            expectedResult: '插件正常工作，无错误日志',
          },
        ],
      },
    };

    return guide;
  }

  /**
   * 生成使用示例
   */
  private async generateUsageExamples(apiEndpoints: any[]): Promise<CodeExample[]> {
    const examples: CodeExample[] = [];

    if (apiEndpoints.length > 0) {
      examples.push({
        title: 'API 调用示例',
        description: '演示如何调用插件 API',
        language: 'typescript',
        code: `// 示例：${apiEndpoints[0].description}
const result = await plugin.get('${apiEndpoints[0].path}');
console.log(result);`,
      });
    }

    examples.push({
      title: '错误处理示例',
      description: '演示如何处理 API 错误',
      language: 'typescript',
      code: `try {
  const result = await plugin.get('/api/data');
  // 处理成功响应
} catch (error) {
  console.error('API request failed:', error);
  // 处理错误
}`,
    });

    return examples;
  }

  /**
   * 验证插件配置
   */
  async validatePluginConfig(config: any): Promise<{ valid: boolean; errors: string[] }> {
    const errors: string[] = [];

    if (!config.id) {
      errors.push('插件 ID 不能为空');
    }

    if (!config.name) {
      errors.push('插件名称不能为空');
    }

    if (!config.version) {
      errors.push('插件版本不能为空');
    }

    if (config.permissions && !Array.isArray(config.permissions)) {
      errors.push('权限配置必须是数组');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * 生成插件 README 文档
   */
  async generateReadme(templateId: string, pluginName: string): Promise<string> {
    const template = await this.getTemplateById(templateId);
    if (!template) {
      throw new Error(`Template not found: ${templateId}`);
    }

    return `# ${pluginName}

${template.description}

## 安装

\`\`\`bash
npm install ${this.kebabCase(pluginName)}
\`\`\`

## 配置

\`\`\`typescript
import Plugin from '${this.kebabCase(pluginName)}';

const plugin = new Plugin({
  id: '${this.kebabCase(pluginName)}',
  name: '${pluginName}',
  version: '1.0.0',
  settings: {
    // 配置你的插件参数
  }
});
\`\`\`

## 使用

\`\`\`typescript
await plugin.initialize();
const result = await plugin.handle({ /* 你的数据 */ });
\`\`\`

## 开发

\`\`\`bash
npm run dev
\`\`\`

## 构建

\`\`\`bash
npm run build
\`\`\`

## 许可证

MIT
`;
  }
}
