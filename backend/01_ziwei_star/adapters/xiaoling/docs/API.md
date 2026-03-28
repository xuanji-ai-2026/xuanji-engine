# 小灵（Xiaoling）API 接口文档

## 概述

小灵（Xiaoling）是管理端智能助手适配层，为管理端提供系统总控、运营管理、UI配置、用户管理和数据统计等功能。

**基础URL:** `http://localhost:5000/api/xiaoling`
**WebSocket URL:** `ws://localhost:5000/xiaoling`

---

## 1. 系统总控接口

### 1.1 获取系统状态

**接口:** `GET /system/status`

**响应:**
```json
{
  "success": true,
  "data": {
    "status": "running",
    "uptime": 123456789,
    "version": "2.1.0",
    "environment": "development"
  },
  "timestamp": 1711234567890
}
```

### 1.2 获取所有服务状态

**接口:** `GET /system/services`

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "name": "api-gateway",
      "status": "running",
      "cpu": 45.2,
      "memory": 52.8,
      "connections": 1243
    }
  ],
  "timestamp": 1711234567890
}
```

### 1.3 获取单个服务状态

**接口:** `GET /system/services/{serviceName}`

**参数:**
- `serviceName`: 服务名称

**响应:**
```json
{
  "success": true,
  "data": {
    "name": "api-gateway",
    "status": "running",
    "cpu": 45.2,
    "memory": 52.8,
    "connections": 1243
  },
  "timestamp": 1711234567890
}
```

### 1.4 控制服务启停

**接口:** `POST /system/control`

**请求体:**
```json
{
  "serviceName": "api-gateway",
  "action": "restart",
  "force": false
}
```

**参数:**
- `serviceName`: 服务名称
- `action`: `start` | `stop` | `restart`
- `force`: 是否强制执行（可选）

**响应:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "message": "Service api-gateway restarted successfully"
  },
  "timestamp": 1711234567890
}
```

### 1.5 获取性能指标

**接口:** `GET /system/metrics?start={start}&end={end}`

**参数:**
- `start`: 开始时间戳（可选）
- `end`: 结束时间戳（可选）

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": 1711234567890,
      "cpu": 45.2,
      "memory": 52.8,
      "disk": 67.3,
      "network": {
        "inbound": 1024000,
        "outbound": 819200
      },
      "requests": {
        "total": 10000,
        "success": 9800,
        "error": 200,
        "avgResponseTime": 250
      }
    }
  ],
  "timestamp": 1711234567890
}
```

---

## 2. 运营管理接口

### 2.1 获取用户活跃度

**接口:** `GET /operations/activities?start={start}&end={end}`

**参数:**
- `start`: 开始时间戳
- `end`: 结束时间戳

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "userId": "user-001001",
      "username": "zhangsan",
      "lastActive": 1711234567890,
      "sessionCount": 45,
      "totalDuration": 7200,
      "dailyActions": 234,
      "weeklyActions": 1567,
      "monthlyActions": 6234
    }
  ],
  "timestamp": 1711234567890
}
```

### 2.2 获取活跃度分析

**接口:** `GET /operations/analytics/{period}`

**参数:**
- `period`: `daily` | `weekly` | `monthly`

**响应:**
```json
{
  "success": true,
  "data": {
    "period": "daily",
    "activeUsers": 1200,
    "newUsers": 50,
    "returningUsers": 1150,
    "averageSessionDuration": 1200,
    "peakHours": [9, 10, 14, 15, 20, 21],
    "topActions": [
      { "action": "view_dashboard", "count": 1234 },
      { "action": "search_user", "count": 892 }
    ]
  },
  "timestamp": 1711234567890
}
```

### 2.3 获取运营策略建议

**接口:** `GET /operations/strategies?category={category}`

**参数:**
- `category`: 类别筛选（可选）`user_retention` | `engagement` | `conversion` | `support`

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "id": "strategy-001001",
      "title": "提升用户留存率",
      "description": "通过个性化推荐和推送通知提高用户留存",
      "priority": "high",
      "category": "user_retention",
      "metrics": {
        "expectedImpact": "+15%",
        "difficulty": "medium",
        "estimatedCost": "¥50,000"
      },
      "actions": [
        "实现个性化内容推荐算法",
        "优化用户首次使用流程"
      ]
    }
  ],
  "timestamp": 1711234567890
}
```

### 2.4 生成数据报表

**接口:** `POST /operations/reports`

**请求体:**
```json
{
  "type": "user_activity",
  "period": {
    "start": 1711234567890,
    "end": 1711320967890
  },
  "metrics": ["active_users", "new_users", "session_duration"],
  "format": "excel",
  "filters": {
    "role": "user"
  }
}
```

**响应:**
```json
{
  "success": true,
  "data": {
    "url": "https://example.com/reports/report-123.xlsx",
    "id": "report-123"
  },
  "timestamp": 1711234567890
}
```

---

## 3. UI配置接口

### 3.1 获取主题配置

**接口:** `GET /ui/themes/{themeId}`

**参数:**
- `themeId`: 主题ID

**响应:**
```json
{
  "success": true,
  "data": {
    "id": "light",
    "name": "浅色主题",
    "colors": {
      "primary": "#1890ff",
      "secondary": "#52c41a",
      "background": "#ffffff"
    },
    "typography": {
      "fontFamily": "Inter, sans-serif",
      "fontSize": {
        "xs": "12px",
        "sm": "14px",
        "md": "16px"
      }
    },
    "spacing": {
      "xs": 4,
      "sm": 8,
      "md": 16
    },
    "borderRadius": {
      "sm": 4,
      "md": 8
    },
    "shadows": true
  },
  "timestamp": 1711234567890
}
```

### 3.2 获取所有主题

**接口:** `GET /ui/themes`

### 3.3 更新主题配置

**接口:** `PATCH /ui/themes/{themeId}`

**请求体:** 部分主题配置

### 3.4 获取布局配置

**接口:** `GET /ui/layouts/{layoutName}`

**响应:**
```json
{
  "success": true,
  "data": {
    "name": "default",
    "description": "默认布局",
    "structure": {
      "header": {
        "enabled": true,
        "height": 64,
        "fixed": true
      },
      "sidebar": {
        "enabled": true,
        "width": 256,
        "collapsible": true,
        "position": "left"
      },
      "footer": {
        "enabled": true,
        "height": 48,
        "fixed": false
      }
    },
    "breakpoints": {
      "mobile": 768,
      "tablet": 1024,
      "desktop": 1280
    }
  },
  "timestamp": 1711234567890
}
```

### 3.5 获取所有布局

**接口:** `GET /ui/layouts`

### 3.6 更新布局配置

**接口:** `PATCH /ui/layouts/{layoutName}`

### 3.7 预览UI效果

**接口:** `POST /ui/preview`

**请求体:**
```json
{
  "theme": "light",
  "layout": "default",
  "screen": "desktop",
  "data": {
    "title": "示例页面",
    "content": "这是UI预览内容"
  }
}
```

**响应:**
```json
{
  "success": true,
  "data": {
    "screenshot": "data:image/png;base64,...",
    "html": "<!DOCTYPE html>..."
  },
  "timestamp": 1711234567890
}
```

---

## 4. 用户管理接口

### 4.1 获取用户信息

**接口:** `GET /users/{userId}`

**响应:**
```json
{
  "success": true,
  "data": {
    "id": "user-001001",
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "phone": "+86138****8888",
    "avatar": "https://example.com/avatar/001.png",
    "role": "admin",
    "status": "active",
    "createdAt": 1711234567890,
    "lastLogin": 1711320967890,
    "metadata": {}
  },
  "timestamp": 1711234567890
}
```

### 4.2 搜索用户

**接口:** `GET /users/search?query={query}&role={role}&status={status}`

**参数:**
- `query`: 搜索关键词
- `role`: 角色筛选（可选）
- `status`: 状态筛选（可选）

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "id": "user-001001",
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "role": "admin",
      "status": "active"
    }
  ],
  "timestamp": 1711234567890
}
```

### 4.3 获取用户列表（分页）

**接口:** `GET /users?page={page}&pageSize={pageSize}&role={role}`

**参数:**
- `page`: 页码（从1开始）
- `pageSize`: 每页数量
- `role`: 角色筛选（可选）

**响应:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "pageSize": 20
  },
  "timestamp": 1711234567890
}
```

### 4.4 获取用户行为分析

**接口:** `GET /users/{userId}/behavior`

**响应:**
```json
{
  "success": true,
  "data": {
    "userId": "user-001001",
    "actions": [
      {
        "type": "view",
        "timestamp": 1711234567890,
        "details": {
          "page": "/dashboard",
          "element": "button"
        }
      }
    ],
    "patterns": {
      "mostActiveTime": "14:00-16:00",
      "favoriteFeatures": ["dashboard", "reports"],
      "averageSessionDuration": 1800
    },
    "riskLevel": "low"
  },
  "timestamp": 1711234567890
}
```

### 4.5 批量用户操作

**接口:** `POST /users/batch`

**请求体:**
```json
{
  "operation": "activate",
  "userIds": ["user-001001", "user-001002", "user-001003"],
  "params": {},
  "dryRun": false
}
```

**参数:**
- `operation`: `activate` | `deactivate` | `ban` | `unban` | `delete` | `update_role`
- `userIds`: 用户ID数组
- `params`: 操作参数（可选）
- `dryRun`: 是否模拟执行（可选）

**响应:**
```json
{
  "success": true,
  "data": {
    "processed": 3,
    "failed": 0,
    "results": [
      {
        "userId": "user-001001",
        "success": true,
        "message": "Success"
      }
    ]
  },
  "timestamp": 1711234567890
}
```

---

## 5. 数据统计接口

### 5.1 查询统计数据

**接口:** `POST /statistics/query`

**请求体:**
```json
{
  "metric": "active_users",
  "period": {
    "start": 1711234567890,
    "end": 1711320967890
  },
  "granularity": "day",
  "filters": {
    "role": "user"
  },
  "groupBy": ["region"]
}
```

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": 1711234567890,
      "value": 1200,
      "metadata": {
        "region": "beijing"
      }
    }
  ],
  "timestamp": 1711234567890
}
```

### 5.2 获取趋势分析

**接口:** `GET /statistics/trend/{metric}?start={start}&end={end}`

**参数:**
- `metric`: 指标名称
- `start`: 开始时间戳
- `end`: 结束时间戳

**响应:**
```json
{
  "success": true,
  "data": {
    "metric": "active_users",
    "current": 1200,
    "previous": 1000,
    "change": 200,
    "changePercent": 20,
    "trend": "up",
    "data": [
      {
        "timestamp": 1711234567890,
        "value": 1000
      }
    ],
    "prediction": [
      {
        "timestamp": 1711407367890,
        "value": 1400
      }
    ]
  },
  "timestamp": 1711234567890
}
```

### 5.3 创建自定义报表

**接口:** `POST /statistics/reports`

**请求体:**
```json
{
  "name": "月度用户增长报表",
  "description": "追踪每月用户增长情况",
  "query": {
    "metric": "new_users",
    "period": {
      "start": 1711234567890,
      "end": 1713902967890
    },
    "granularity": "month"
  },
  "visualization": {
    "type": "line",
    "config": {
      "showArea": true,
      "smooth": true
    }
  },
  "schedule": {
    "enabled": true,
    "frequency": "monthly",
    "recipients": ["admin@example.com"]
  }
}
```

**响应:**
```json
{
  "success": true,
  "data": {
    "id": "report-001001",
    "name": "月度用户增长报表",
    ...
  },
  "timestamp": 1711234567890
}
```

### 5.4 获取自定义报表

**接口:** `GET /statistics/reports/{reportId}`

### 5.5 获取所有自定义报表

**接口:** `GET /statistics/reports`

### 5.6 更新自定义报表

**接口:** `PATCH /statistics/reports/{reportId}`

### 5.7 删除自定义报表

**接口:** `DELETE /statistics/reports/{reportId}`

---

## WebSocket 事件

### 连接事件

**事件类型:** `connected`

```json
{
  "type": "connected",
  "timestamp": 1711234567890
}
```

**事件类型:** `disconnected`

```json
{
  "type": "disconnected",
  "timestamp": 1711234567890
}
```

###**事件类型:** `error`

```json
{
  "type": "error",
  "error": {
    "code": "CONNECTION_ERROR",
    "message": "Connection failed"
  },
  "timestamp": 1711234567890
}
```

### 数据推送事件

**事件类型:** `system:metrics`

```json
{
  "type": "system:metrics",
  "payload": {
    "cpu": 45.2,
    "memory": 52.8,
    "timestamp": 1711234567890
  }
}
```

**事件类型:** `users:activity`

```json
{
  "type": "users:activity",
  "payload": {
    "activeUsers": 1200,
    "timestamp": 1711234567890
  }
}
```

---

## 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}
  },
  "timestamp": 1711234567890
}
```

### 常见错误码

| 错误码 | 描述 |
|--------|------|
| `INVALID_REQUEST` | 请求参数错误 |
| `UNAUTHORIZED` | 未授权访问 |
| `NOT_FOUND` | 资源不存在 |
| `NETWORK_ERROR` | 网络连接错误 |
| `INTERNAL_ERROR` | 服务器内部错误 |

---

## 速率限制

- 默认限制: 1000 请求/小时/IP
- 超出限制返回 `429 Too Many Requests`

---

## 版本

当前版本: `v1.0.0`
