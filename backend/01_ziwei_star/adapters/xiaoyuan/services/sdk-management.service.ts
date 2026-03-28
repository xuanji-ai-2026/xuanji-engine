/**
 * 小元 - SDK 管理服务
 * 提供 SDK 版本管理、集成指导、更新提醒等功能
 */

import {
  SdkVersion,
  SdkInfo,
  SdkIntegrationGuide,
  SdkUpdate,
  CodeExample,
  ConfigurationStep,
} from '../types';

export class SdkManagementService {
  private sdks: Map<string, SdkInfo> = new Map();
  private config: any;
  private logger: any;
  private checkInterval?: NodeJS.Timeout;

  constructor(config: any, logger: any) {
    this.config = config;
    this.logger = logger;
    this.initializeSdks();
  }

  /**
   * 初始化 SDK 信息
   */
  private initializeSdks(): void {
    // JavaScript SDK
    this.registerSdk({
      name: 'javascript',
      currentVersion: '1.2.0',
      latestVersion: '1.2.0',
      versions: [
        {
          name: 'JavaScript SDK',
          version: '1.2.0',
          releaseDate: '2026-03-01',
          type: 'minor',
          changelog: [
            '新增批量操作 API',
            '优化错误处理机制',
            '改进类型定义',
          ],
          downloadUrl: 'https://cdn.example.com/sdk/js/v1.2.0/xuanji.js',
        },
        {
          name: 'JavaScript SDK',
          version: '1.1.0',
          releaseDate: '2026-02-15',
          type: 'minor',
          changelog: [
            '添加 WebSocket 支持',
            '新增事件监听器',
            '性能优化',
          ],
          downloadUrl: 'https://cdn.example.com/sdk/js/v1.1.0/xuanji.js',
        },
        {
          name: 'JavaScript SDK',
          version: '1.0.0',
          releaseDate: '2026-01-01',
          type: 'major',
          changelog: [
            '首个正式版本发布',
            '完整的 API 支持',
            'TypeScript 类型定义',
          ],
          downloadUrl: 'https://cdn.example.com/sdk/js/v1.0.0/xuanji.js',
        },
      ],
      platforms: ['Node.js', 'Browser'],
      languages: ['JavaScript', 'TypeScript'],
      documentationUrl: 'https://docs.xuanji.ai/sdk/javascript',
      repositoryUrl: 'https://github.com/xuanji-ai/javascript-sdk',
    });

    // Python SDK
    this.registerSdk({
      name: 'python',
      currentVersion: '1.1.0',
      latestVersion: '1.1.0',
      versions: [
        {
          name: 'Python SDK',
          version: '1.1.0',
          releaseDate: '2026-03-10',
          type: 'minor',
          changelog: [
            '新增异步支持',
            '改进连接池管理',
            '添加更多工具函数',
          ],
          downloadUrl: 'https://pypi.org/project/xuanji-sdk/1.1.0/',
        },
        {
          name: 'Python SDK',
          version: '1.0.0',
          releaseDate: '2026-01-15',
          type: 'major',
          changelog: [
            '首个正式版本发布',
            '完整的 API 封装',
            '错误处理优化',
          ],
          downloadUrl: 'https://pypi.org/project/xuanji-sdk/1.0.0/',
        },
      ],
      platforms: ['Python 3.8+', 'Python 3.9+', 'Python 3.10+', 'Python 3.11+'],
      languages: ['Python'],
      documentationUrl: 'https://docs.xuanji.ai/sdk/python',
      repositoryUrl: 'https://github.com/xuanji-ai/python-sdk',
    });

    // TypeScript SDK
    this.registerSdk({
      name: 'typescript',
      currentVersion: '1.2.0',
      latestVersion: '1.2.0',
      versions: [
        {
          name: 'TypeScript SDK',
          version: '1.2.0',
          releaseDate: '2026-03-05',
          type: 'minor',
          changelog: [
            '完整的类型定义',
            '泛型支持',
            'ES6+ 模块导出',
          ],
          downloadUrl: 'https://www.npmjs.com/package/@xuanji-ai/sdk',
        },
        {
          name: 'TypeScript SDK',
          version: '1.1.0',
          releaseDate: '2026-02-20',
          type: 'minor',
          changelog: [
            '改进类型推断',
            '添加更多工具类型',
            '文档完善',
          ],
          downloadUrl: 'https://www.npmjs.com/package/@xuanji-ai/sdk',
        },
        {
          name: 'TypeScript SDK',
          version: '1.0.0',
          releaseDate: '2026-01-10',
          type: 'major',
          changelog: [
            '首个正式版本',
            '完整的 TypeScript 类型支持',
            '类型安全的 API 调用',
          ],
          downloadUrl: 'https://www.npmjs.com/package/@xuanji-ai/sdk',
        },
      ],
      platforms: ['Node.js', 'Browser'],
      languages: ['TypeScript'],
      documentationUrl: 'https://docs.xuanji.ai/sdk/typescript',
      repositoryUrl: 'https://github.com/xuanji-ai/typescript-sdk',
    });
  }

  /**
   * 注册 SDK
   */
  private registerSdk(sdk: SdkInfo): void {
    this.sdks.set(sdk.name, sdk);
    this.logger.debug(`Registered SDK: ${sdk.name}`);
  }

  /**
   * 获取所有 SDK
   */
  async getAllSdks(): Promise<SdkInfo[]> {
    return Array.from(this.sdks.values());
  }

  /**
   * 根据 name 获取 SDK
   */
  async getSdkByName(name: string): Promise<SdkInfo | null> {
    return this.sdks.get(name) || null;
  }

  /**
   * 检查 SDK 更新
   */
  async checkUpdates(sdkName: string): Promise<SdkUpdate | null> {
    const sdk = this.sdks.get(sdkName);
    if (!sdk) {
      throw new Error(`SDK not found: ${sdkName}`);
    }

    // 检查是否有新版本
    if (sdk.currentVersion === sdk.latestVersion) {
      this.logger.debug(`SDK ${sdkName} is up to date: ${sdk.currentVersion}`);
      return null;
    }

    const currentVersion = this.findVersion(sdk, sdk.currentVersion);
    const latestVersion = this.findVersion(sdk, sdk.latestVersion);

    if (!latestVersion) {
      return null;
    }

    const update: SdkUpdate = {
      sdkName,
      fromVersion: sdk.currentVersion,
      toVersion: sdk.latestVersion,
      type: latestVersion.type,
      changes: latestVersion.changelog,
      breakingChanges: latestVersion.breakingChanges || [],
      migrationGuide: await this.generateMigrationGuide(sdkName, sdk.currentVersion, sdk.latestVersion),
    };

    return update;
  }

  /**
   * 查找特定版本
   */
  private findVersion(sdk: SdkInfo, version: string): SdkVersion | undefined {
    return sdk.versions.find(v => v.version === version);
  }

  /**
   * 生成迁移指南
   */
  private async generateMigrationGuide(sdkName: string, fromVersion: string, toVersion: string): Promise<CodeExample[]> {
    const guides: CodeExample[] = [];

    guides.push({
      title: '更新 SDK 版本',
      description: `从 ${fromVersion} 更新到 ${toVersion}`,
      language: sdkName === 'python' ? 'bash' : 'bash',
      code: sdkName === 'python' 
        ? `pip install --upgrade xuanji-sdk==${toVersion}`
        : `npm install @xuanji-ai/sdk@${toVersion}`,
    });

    // 如果有破坏性变更，添加迁移示例
    guides.push({
      title: '更新后的代码调整',
      description: '根据新版本调整代码可能需要的修改',
      language: sdkName === 'python' ? 'python' : 'typescript',
      code: sdkName === 'python'
        ? `# 检查查文档了解 API 变更
# 查看迁移指南: https://docs.xuanji.ai/sdk/python/migration`
        : `// 检查 TypeScript 类型变化
// 查看迁移指南: https://docs.xuanji.ai/sdk/typescript/migration`,
    });

    return guides;
  }

  /**
   * 启动自动更新检查
   */
  startUpdateCheck(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }

    const interval = this.config.services.sdkManagement.checkUpdatesInterval || 86400000;

    this.checkInterval = setInterval(async () => {
      this.logger.debug('Checking SDK updates...');
      for (const [name, sdk] of this.sdks) {
        try {
          const update = await this.checkUpdates(name);
          if (update) {
            this.logger.warn(`SDK ${name} has update available: ${update.toVersion}`);
            // 这里可以触发通知事件
          }
        } catch (error) {
          this.logger.error(`Failed to check updates for ${name}: ${error}`);
        }
      }
    }, interval);

    this.logger.info(`SDK update check started (interval: ${interval}ms)`);
  }

  /**
   * 停止自动更新检查
   */
  stopUpdateCheck(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = undefined;
      this.logger.info('SDK update check stopped');
    }
  }

  /**
   * 生成集成指南
   */
  async generateIntegrationGuide(sdkName: string, platform: string, language: string): Promise<SdkIntegrationGuide> {
    const sdk = this.sdks.get(sdkName);
    if (!sdk) {
      throw new { message: `SDK not found: ${sdkName}` };
    }

    const guide: SdkIntegrationGuide = {
      sdkName,
      platform,
      language,
      installationSteps: this.getInstallationSteps(sdkName, platform),
      configurationSteps: await this.getConfigurationSteps(sdkName, platform),
      usageExamples: await this.getUsageExamples(sdkName, language),
      commonIssues: this.getCommonIssues(sdkName),
    };

    return guide;
  }

  /**
   * 获取安装步骤
   */
  private getInstallationSteps(sdkName: string, platform: string): string[] {
    const steps: string[] = [];

    if (sdkName === 'python') {
      steps.push('pip install xuanji-sdk');
      steps.push('验证安装: pip show xuanji-sdk');
    } else {
      steps.push('npm install @xuanji-ai/sdk');
      steps.push('验证安装: npm list @xuanji-ai/sdk');
    }

    if (platform === 'Node.js') {
      steps.push('确保 Node.js 版本 >= 14');
    } else if (platform.includes('Python')) {
      steps.push('确保 Python 版本 >= 3.8');
    }

    return steps;
  }

  /**
   * 获取配置步骤
   */
  private async getConfigurationSteps(sdkName: string, platform: string): Promise<ConfigurationStep[]> {
    const steps: ConfigurationStep[] = [
      {
        step: 1,
        title: '获取 API Key',
        description: '在控制台获取你的 API Key',
      },
      {
        step: 2,
        title: '创建配置文件',
        description: '创建 SDK 配置文件',
        files: [
          {
            path: sdkName === 'python' ? 'xuanji_config.py' : 'xuanji.config.ts',
            content: sdkName === 'python'
              ? `# Xuanji SDK Configuration
XUANJI_API_KEY = "your-api-key"
XUANJI_API_URL = "https://api.xuanji.ai/v1"
XUANJI_TIMEOUT = 30`
              : `// Xuanji SDK Configuration
export const xuanjiConfig = {
  apiKey: 'your-api-key',
  apiUrl: 'https://api.xuanji.ai/v1',
  timeout: 30000,
};`,
          },
        ],
      },
      {
        step: 3,
        title: '初始化 SDK',
        description: '在应用中初始化 SDK',
        code: sdkName === 'python'
          ? `from xuanji_sdk import Xuanji

client = Xuanji(
    api_key="your-api-key",
    base_url="https://api.xuanji.ai/v1"
)`
          : `import { Xuanji } from '@xuanji-ai/sdk';

const client = new Xuanji({
  apiKey: 'your-api-key',
  apiUrl: 'https://api.xuanji.ai/v1',
});`,
      },
    ];

    return steps;
  }

  /**
   * 获取使用示例
   */
  private async getUsageExamples(sdkName: string, language: string): Promise<CodeExample[]> {
    const examples: CodeExample[] = [];

    const isPython = sdkName === 'python';

    examples.push({
      title: '基础使用',
      description: 'SDK 的基本使用方法',
      language,
      code: isPython
        ? `# 导入 SDK
from xuanji_sdk import Xuanji

# 创建客户端
client = Xuanji(api_key="your-api-key")

# 调用 API
response = client.chat.completions.create(
    model="xuanji-1",
    messages=[
        {"role": "user", "content": "Hello, Xuanji!"}
    ]
)

print(response.choices[0].message.content)`
        : `import { Xuanji } from '@xuanji-ai/sdk';

// 创建客户端
const client = new Xuanji({
  apiKey: 'your-api-key',
});

// 调用 API
const response = await client.chat.completions.create({
  model: 'xuanji-1',
  messages: [
    { role: 'user', content: 'Hello, Xuanji!' }
  ],
});

console.log(response.choices[0].message.content);`,
    });

    examples.push({
      title: '流式响应',
      description: '处理流式 API 响应',
      language,
      code: isPython
        ? `# 流式响应
stream = client.chat.completions.create(
    model="xuanji-1",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")`
        : `// 流式响应
const stream = await client.chat.completions.create({
  model: 'xuanji-1',
  messages: [
    { role: 'user', content: 'Tell me a story' }
  ],
  stream: true,
});

for await (const chunk of stream) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}`,
    });

    examples.push({
      title: '错误处理',
      description: '正确处理 API 错误',
      language,
      code: isPython
        ? `from xuanji_sdk import Xuanji, XuanjiError

try:
    response = client.chat.completions.create(
        model="xuanji-1.0",
        messages=[{"role": "user", "content": "Hello"}]
    )
except XuanjiError as e:
    print(f"Error: {e.message}")
    print(f"Status: {e.status_code}")
    print(f"Details: {e.details}")`
        : `import { Xuanji, XuanjiError } from '@xuanji-ai/sdk';

try {
  const response = await client.chat.completions.create({
    model: 'xuanji-1.0',
    messages: [{ role: 'user', content: 'Hello' }],
  });
} catch (error) {
  if (error instanceof XuanjiError) {
    console.error('Error:', error.message);
    console.error('Status:', error.statusCode);
    console.error('Details:', error.details);
  }
}`,
    });

    return examples;
  }

  /**
   * 获取常见问题
   */
  private getCommonIssues(sdkName: string): Array<{ title: string; description: string; solution: string; code?: string }> {
    const issues: Array<{ title: string; description: string; solution: string; code?: string }> = [];

    issues.push({
      title: 'API Key 无效',
      description: '收到 401 或 API Key 错误',
      solution: '检查 API Key 是否正确，是否已激活，是否有足够的权限',
    });

    issues.push({
      title: '连接超时',
      description: '请求响应时间过长',
      solution: '检查网络连接，增加超时时间配置，或使用重试机制',
      code: sdkName === 'python'
        ? `client = Xuanji(api_key="your-api-key", timeout=60)`
        : `const client = new Xuanji({
  apiKey: 'your-api-key',
  timeout: 60000,
});`,
    });

    issues.push({
      title: '版本不兼容',
      description: 'SDK 版本与 API 版本不匹配',
      solution: '更新 SDK 到最新版本，或使用兼容的 API 版本',
      code: sdkName === 'python'
        ? `pip install --upgrade xuanji-sdk`
        : `npm update @xuanji-ai/sdk`,
    });

    issues.push({
      title: '内存不足',
      description: '处理大量数据时内存溢出',
      solution: '使用流式处理或分批处理数据',
      code: sdkName === 'python'
        ? `# 使用流式处理
for item in client.process_stream(large_data):
    handle_item(item)`
        : `// 使用流式处理
for await (const item of client.processStream(largeData)) {
  handleItem(item);
}`,
}`,
    });

    return issues;
  }

  /**
   * 获取 SDK 版本历史
   */
  async getVersionHistory(sdkName: string): Promise<SdkVersion[]> {
    const sdk = this.sdks.get(sdkName);
    if (!sdk) {
      throw new Error(`SDK not found: ${sdkName}`);
    }
    return sdk.versions;
  }

  /**
   * 比较版本
   */
  private compareVersions(v1: string, v2: string): number {
    const parts1 = v1.split('.').map(Number);
    const parts2 = v2.split('.').map(Number);

    for (let i = 0; i < Math.max(parts1.length, parts2.length); i++) {
      const p1 = parts1[i] || 0;
      const p2 = parts2[i] || 0;

      if (p1 > p2) return 1;
      if (p1 < p2) return -1;
    }

    return 0;
  }
}
