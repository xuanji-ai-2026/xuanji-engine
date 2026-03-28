/**
 * 小微适配层 - 统一入口
 * 版本: v1.0.0
 * 描述: 配置端智能助手适配层统一入口
 */

import { XiaoweiConfig, WebSocketEvents } from '../types';
import { ConfigAdapter } from './ConfigAdapter';
import { WorkbenchHelper } from './WorkbenchHelper';
import { AuthHelper } from './AuthHelper';
import { UserHelper } from './UserHelper';

export class XiaoweiAdapter {
  private configAdapter: ConfigAdapter;
  private workbenchHelper: WorkbenchHelper;
  private authHelper: AuthHelper;
  private userHelper: UserHelper;

  constructor(config: XiaoweiConfig) {
    this.configAdapter = new ConfigAdapter(config);
    this.workbenchHelper = new WorkbenchHelper(this.configAdapter);
    this.authHelper = new AuthHelper(this.configAdapter);
    this.userHelper = new UserHelper(this.configAdapter);
  }

  /**
   * 连接到紫微元灵核心
   */
  async connect(events?: WebSocketEvents): Promise<void> {
    return this.configAdapter.connect(events);
  }

  /**
   * 断开连接
   */
  disconnect(): void {
    this.configAdapter.disconnect();
  }

  /**
   * 获取配置助手
   */
  get config() {
    return this.configAdapter;
  }

  /**
   * 获取工作台助手
   */
  get workbench() {
    return this.workbenchHelper;
  }

  /**
   * 获取认证助手
   */
  get auth() {
    return this.authHelper;
  }

  /**
   * 获取用户管理助手
   */
  get user() {
    return this.userHelper;
  }
}

/**
 * 工厂函数 - 创建小微适配器实例
 */
export function createXiaoweiAdapter(config: Partial<XiaoweiConfig>): XiaoweiAdapter {
  const defaultConfig: XiaoweiConfig = {
    coreWsUrl: config.coreWsUrl || 'ws://localhost:8001/ws',
    coreHttpUrl: config.coreHttpUrl || 'http://localhost:8001',
    adapterId: config.adapterId || 'xiaowei-adapter',
    authToken: config.authToken || '',
    logLevel: config.logLevel || 'info',
    timeout: config.timeout || 30000
  };

  return new XiaoweiAdapter(defaultConfig);
}

// 导出所有类和类型
export { ConfigAdapter, WorkbenchHelper, AuthHelper, UserHelper };
export * from '../types';

export default XiaoweiAdapter;
