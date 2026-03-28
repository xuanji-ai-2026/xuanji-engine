/**
 * 小灵（Xiaoling）React 集成示例
 * 展示如何在 React 应用中使用小灵适配层
 */

import React, { useEffect, useState, useCallback } from 'react';
import { XiaolingAdapter } from '../src/XiaolingAdapter';
import type {
  SystemStatus,
  ServiceStatus,
  UserActivity,
  ThemeConfig,
} from '../types/xiaoling.types';

// ==================== 1. 创建小灵实例 ====================

const xiaoling = new XiaolingAdapter({
  websocket: {
    enabled: true,
    url: 'ws://localhost:5000/xiaoling',
    reconnectInterval: 3000,
    maxRetries: 5,
  },
  http: {
    baseUrl: 'http://localhost:5000/api/xiaoling',
    timeout: 10000,
    maxRetries: 3,
  },
});

// ==================== 2. 系统状态监控组件 ====================

export function SystemStatusMonitor() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [serviceStatuses, setServiceStatuses] = useState<ServiceStatus[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setLoading(true);

    try {
      const [statusResult, servicesResult] = await Promise.all([
        xiaoling.getSystemStatus(),
        xiaoling.getServiceStatuses(),
      ]);

      if (statusResult.success && statusResult.data) {
        setSystemStatus(statusResult.data);
      }

      if (servicesResult.success && servicesResult.data) {
        setServiceStatuses(servicesResult.data);
      }
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();

    // 每30秒自动刷新
    const interval = setInterval(fetchData, 30000);

    return () => clearInterval(interval);
  }, [fetchData]);

  // 监听WebSocket事件
  useEffect(() => {
    const handleMetricsUpdate = (data: any) => {
      console.log('Metrics updated:', data);
    };

    xiaoling.on('system:metrics', handleMetricsUpdate);

    return () => {
      xiaoling.off('system:metrics', handleMetricsUpdate);
    };
  }, []);

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div className="system-status-monitor">
      <h2>系统状态监控</h2>

      {systemStatus && (
        <div className="system-overview">
          <p>状态: {systemStatus.status}</p>
          <p>运行时间: {Math.floor(systemStatus.uptime / 3600)} 小时</p>
          <p>版本: {systemStatus.version}</p>
          <p>环境: {systemStatus.environment}</p>
        </div>
      )}

      <h3>服务状态</h3>
      <div className="services-grid">
        {serviceStatuses.map((service) => (
          <div key={service.name} className="service-card">
            <h4>{service.name}</h4>
            <p>状态: {service.status}</p>
            <p>CPU: {service.cpu.toFixed(1)}%</p>
            <p>内存: {service.memory.toFixed(1)}%</p>
            <p>连接数: {service.connections}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// ==================== 3. 用户活跃度分析组件 ====================

export function UserActivityAnalytics() {
  const [activities, setActivities] = useState<UserActivity[]>([]);
  const [period, setPeriod] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [loading, setLoading] = useState(false);

  const fetchActivities = useCallback(async () => {
    setLoading(true);

    const now = Date.now();
    const start = now - (period === 'daily' ? 86400000 : period === 'weekly' ? 604800000 : 2592000000);

    try {
      const result = await xiaoling.getUserActivities({ start, end: now });

      if (result.success && result.data) {
        setActivities(result.data);
      }
    } catch (error) {
      console.error('Failed to fetch user activities:', error);
    } finally {
      setLoading(false);
    }
  }, [period]);

  useEffect(() => {
    fetchActivities();
  }, [fetchActivities]);

  return (
    <div className="user-activity-analytics">
      <h2>用户活跃度分析</h2>

      <div className="period-selector">
        <button
          onClick={() => setPeriod('daily')}
          className={period === 'daily' ? 'active' : ''}
        >
          日
        </button>
        <button
          onClick={() => setPeriod('weekly')}
          className={period === 'weekly' ? 'active' : ''}
        >
          周
        </button>
        <button
          onClick={() => setPeriod('monthly')}
          className={period === 'monthly' ? 'active' : ''}
        >
          月
        </button>
      </div>

      {loading ? (
        <p>加载中...</p>
      ) : (
        <table className="activity-table">
          <thead>
            <tr>
              <th>用户</th>
              <th>最后活跃</th>
              <th>会话数</th>
              <th>总时长</th>
              <th>操作数</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity) => (
              <tr key={activity.userId}>
                <td>{activity.username}</td>
                <td>{new Date(activity.lastActive).toLocaleString()}</td>
                <td>{activity.sessionCount}</td>
                <td>{Math.floor(activity.totalDuration / 60)} 分钟</td>
                <td>{activity.dailyActions}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

// ==================== 4. 主题配置组件 ====================

export function ThemeConfigurator() {
  const [themes, setThemes] = useState<ThemeConfig[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<ThemeConfig | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchThemes = async () => {
      setLoading(true);

      try {
        const result = await xiaoling.getThemes();

        if (result.success && result.data) {
          setThemes(result.data);
          setSelectedTheme(result.data[0]);
        }
      } catch (error) {
        console.error('Failed to fetch themes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchThemes();
  }, []);

  const handleThemeChange = async (themeId: string) => {
    try {
      const result = await xiaoling.getTheme(themeId);

      if (result.success && result.data) {
        setSelectedTheme(result.data);
        // 应用主题到应用
        applyTheme(result.data);
      }
    } catch (error) {
      console.error('Failed to load theme:', error);
    }
  };

  const handleColorChange = async (colorKey: string, value: string) => {
    if (!selectedTheme) return;

    const updatedTheme = {
      ...selectedTheme,
      colors: {
        ...selectedTheme.colors,
        [colorKey]: value,
      },
    };

    try {
      const result = await xiaoling.updateTheme(selectedTheme.id, {
        colors: updatedTheme.colors,
      });

      if (result.success && result.data) {
        setSelectedTheme(result.data);
        applyTheme(result.data);
      }
    } catch (error) {
      console.error('Failed to update theme:', error);
    }
  };

  const applyTheme = (theme: ThemeConfig) => {
    // 应用主题CSS变量
    const root = document.documentElement;
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value);
    });
  };

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div className="theme-configurator">
      <h2>主题配置</h2>

      <div className="theme-selector">
        <h3>选择主题</h3>
        <select
          value={selectedTheme?.id || ''}
          onChange={(e) => handleThemeChange(e.target.value)}
        >
          {themes.map((theme) => (
            <option key={theme.id} value={theme.id}>
              {theme.name}
            </option>
          ))}
        </select>
      </div>

      {selectedTheme && (
        <div className="theme-editor">
          <h3>颜色配置</h3>
          {Object.entries(selectedTheme.colors).map(([key, value]) => (
            <div key={key} className="color-input">
              <label>{key}:</label>
              <input
                type="color"
                value={value}
                onChange={(e) => handleColorChange(key, e.target.value)}
              />
              <span>{value}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ==================== 5. 服务控制组件 ====================

export function ServiceController() {
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchServices = async () => {
    setLoading(true);

    try {
      const result = await xiaoling.getServiceStatuses();

      if (result.success && result.data) {
        setServices(result.data);
      }
    } catch (error) {
      console.error('Failed to fetch services:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServices();
  }, []);

  const handleServiceAction = async (serviceName: string, action: 'start' | 'stop' | 'restart') => {
    try {
      const result = await xiaoling.controlService({
        serviceName,
        action,
      });

      if (result.success) {
        alert(result.data?.message || '操作成功');
        await fetchServices();
      } else {
        alert('操作失败: ' + result.error?.message);
      }
    } catch (error) {
      console.error('Failed to control service:', error);
      alert('操作失败');
    }
  };

  if (loading) {
    return <div>加载中...</div>;
  }

  return (
    <div className="service-controller">
      <h2>服务控制</h2>

      <table className="services-table">
        <thead>
          <tr>
            <th>服务名称</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {services.map((service) => (
            <tr key={service.name}>
              <td>{service.name}</td>
              <td>
                <span className={`status ${service.status}`}>
                  {service.status}
                </span>
              </td>
              <td>
                <button
                  onClick={() => handleServiceAction(service.name, 'start')}
                  disabled={service.status === 'running'}
                >
                  启动
                </button>
                <button
                  onClick={() => handleServiceAction(service.name, 'stop')}
                  disabled={service.status === 'stopped'}
                >
                  停止
                </button>
                <button
                  onClick={() => handleServiceAction(service.name, 'restart')}
                  disabled={service.status !== 'running'}
                >
                  重启
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ==================== 6. 统一使用示例 ====================

export default function XiaolingDemoApp() {
  const [activeTab, setActiveTab] = useState<'system' | 'users' | 'theme' | 'services'>('system');

  return (
    <div className="xiaoling-demo-app">
      <h1>小灵（Xiaoling）管理面板</h1>

      <div className="tab-navigation">
        <button
          onClick={() => setActiveTab('system')}
          className={activeTab === 'system' ? 'active' : ''}
        >
          系统监控
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={activeTab === 'users' ? 'active' : ''}
        >
          用户分析
        </button>
        <button
          onClick={() => setActiveTab('theme')}
          className={activeTab === 'theme' ? 'active' : ''}
        >
          主题配置
        </button>
        <button
          onClick={() => setActiveTab('services')}
          className={activeTab === 'services' ? 'active' : ''}
        >
          服务控制
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'system' && <SystemStatusMonitor />}
        {activeTab === 'users' && <UserActivityAnalytics />}
        {activeTab === 'theme' && <ThemeConfigurator />}
        {activeTab === 'services' && <ServiceController />}
      </div>
    </div>
  );
}

// ==================== TypeScript 自定义 Hook 示例 ====================

export function useSystemStatus(refreshInterval = 30000) {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [serviceStatuses, setServiceStatuses] = useState<ServiceStatus[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchStatus = useCallback(async () => {
    setLoading(true);

    try {
      const [statusResult, servicesResult] = await Promise.all([
        xiaoling.getSystemStatus(),
        xiaoling.getServiceStatuses(),
      ]);

      if (statusResult.success && statusResult.data) {
        setSystemStatus(statusResult.data);
      }

      if (servicesResult.success && servicesResult.data) {
        setServiceStatuses(servicesResult.data);
      }
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();

    const interval = setInterval(fetchStatus, refreshInterval);

    return () => clearInterval(interval);
  }, [fetchStatus, refreshInterval]);

  return { systemStatus, serviceStatuses, loading, refetch: fetchStatus };
}
