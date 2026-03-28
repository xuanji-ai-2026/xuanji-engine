# 计费支付模块技术方案设计文档

## 1. 模块概述

### 1.1 模块组成
- **计费引擎 (Billing Engine)**: 负责计费策略计算、费率管理、账单生成
- **支付网关 (Payment Gateway)**: 统一支付接口，支持多种支付渠道
- **发票管理 (Invoice Manager)**: 发票生成、开具、管理
- **财务管理 (Financial Management)**: 财务报表、收支统计、对账

### 1.2 技术栈
- **语言**: Python 3.11+
- **框架**: FastAPI (API服务) + SQLAlchemy (ORM)
- **数据库**: PostgreSQL
- **缓存**: Redis
- **消息队列**: Redis Pub/Sub
- **支付渠道**: 支付宝、微信支付、银联
- **依赖管理**: Poetry

## 2. 架构设计

### 2.1 整体架构
```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway Layer                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┼────────────────────────────────────┐
│                    Business Service Layer                │
├────────────────────┼────────────────────────────────────┤
│  │  ┌──────────┐  │  ┌──────────┐  │  ┌──────────┐  │  │
│  │  │ 计费引擎 │  │  │ 支付网关 │  │  │ 发票管理 │  │  │
│  │  └──────────┘  │  └──────────┘  │  └──────────┘  │  │
│  └────────────────┴────────────────┴────────────────┘  │
│                    财务管理                              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┼────────────────────────────────────┐
│                    Data Access Layer                     │
├────────────────────┼────────────────────────────────────┤
│  PostgreSQL  │  Redis  │  消息队列  │  外部支付接口    │
└─────────────────────────────────────────────────────────┘
```

### 2.2 核心模块设计

#### 2.2.1 计费引擎 (Billing Engine)
**职责**:
- 计费策略配置与加载
- 实时计费计算
- 账单生成与汇总
- 费率版本管理

**核心类**:
- `BillingEngine`: 计费引擎主类
- `BillingStrategy`: 计费策略接口
- `RateCalculator`: 费率计算器
- `InvoiceGenerator`: 发票生成器
- `BillAggregator`: 账单汇总器

**计费模式**:
- 按量计费: 基于使用量 × 单价
- 阶梯计费: 多级阶梯费率
- 时间计费: 基于使用时长
- 套餐计费: 预付费套餐
- 自定义计费: 通过脚本扩展

#### 2.2.2 支付网关 (Payment Gateway)
**职责**:
- 统一支付接口封装
- 多支付渠道适配
- 支付回调处理
- 支付状态同步

**核心类**:
- `PaymentGateway`: 支付网关主类
- `PaymentAdapter`: 支付渠道适配器接口
- `AlipayAdapter`: 支付宝适配器
- `WeChatPayAdapter`: 微信支付适配器
- `UnionPayAdapter`: 银联适配器
- `PaymentCallbackHandler`: 回调处理器

**支付流程**:
1. 创建支付订单 → 生成支付URL
2. 用户支付 → 第三方回调
3. 验证签名 → 更新支付状态
4. 触发业务回调 → 通知业务系统

#### 2.2.3 发票管理 (Invoice Manager)
**职责**:
- 发票信息管理
- 发票生成与打印
- 发票开具（对接税控系统）
- 发票统计与查询

**核心类**:
- `InvoiceManager`: 发票管理器
- `InvoiceGenerator`: 发票生成器
- `InvoiceTemplate`: 发票模板管理
- `TaxSystemClient`: 税控系统客户端

**发票类型**:
- 普通发票
- 增值税专用发票
- 电子发票
- 纸质发票

#### 2.2.4 财务管理 (Financial Management)
**职责**:
- 财务报表生成
- 收支统计分析
- 账单对账
- 财务预警

**核心类**:
- `FinancialManager`: 财务管理器
- `ReportGenerator`: 报表生成器
- `ReconciliationService`: 对账服务
- `AlertService`: 预警服务

**报表类型**:
- 日报表、月报表、年报表
- 收入分析报表
- 渠道分析报表
- 客户贡献报表

## 3. 数据库设计

### 3.1 核心表结构

#### 3.1.1 计费相关表
```sql
-- 计费策略表
CREATE TABLE billing_strategies (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- usage, tiered, time, package, custom
    config JSONB NOT NULL,
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 费率表
CREATE TABLE billing_rates (
    id BIGSERIAL PRIMARY KEY,
    strategy_id BIGINT REFERENCES billing_strategies(id),
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(50),  -- 按量计费单位
    price DECIMAL(10,4) NOT NULL,
    tier_start DECIMAL(10,2),  -- 阶梯起始值
    tier_end DECIMAL(10,2),  -- 阶梯结束值
    effective_date DATE NOT NULL,
    expire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 账单表
CREATE TABLE bills (
    id BIGSERIAL PRIMARY KEY,
    bill_no VARCHAR(50) UNIQUE NOT NULL,
    customer_id BIGINT NOT NULL,
    strategy_id BIGINT REFERENCES billing_strategies(id),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    billing_amount DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'unpaid',  -- unpaid, paid, overdue, cancelled
    items JSONB,  -- 账单明细
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP
);
```

#### 3.1.2 支付相关表
```sql
-- 支付订单表
CREATE TABLE payment_orders (
    id BIGSERIAL PRIMARY KEY,
    order_no VARCHAR(50) UNIQUE NOT NULL,
    bill_id BIGINT REFERENCES bills(id),
    customer_id BIGINT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'CNY',
    channel VARCHAR(20) NOT NULL,  -- alipay, wechat, unionpay
    status VARCHAR(20) DEFAULT 'pending',  -- pending, success, failed, cancelled
    payment_url TEXT,
    transaction_id VARCHAR(100),
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 支付回调记录表
CREATE TABLE payment_callbacks (
    id BIGSERIAL PRIMARY KEY,
    order_no VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    callback_data JSONB NOT NULL,
    signature VARCHAR(500),
    verified BOOLEAN DEFAULT FALSE,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.3 发票相关表
```sql
-- 发票表
CREATE TABLE invoices (
    id BIGSERIAL PRIMARY KEY,
    invoice_no VARCHAR(50) UNIQUE NOT NULL,
    bill_id BIGINT REFERENCES bills(id),
    customer_id BIGINT NOT NULL,
    type VARCHAR(20) NOT NULL,  -- normal, vat_special, electronic, paper
    title VARCHAR(200),  -- 发票抬头
    tax_no VARCHAR(50),  -- 税号
    amount DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(12,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, issued, invalid
    items JSONB,  -- 发票明细
    pdf_url TEXT,  -- 电子发票PDF URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    issued_at TIMESTAMP
);
```

#### 3.1.4 财务相关表
```sql
-- 财务流水表
CREATE TABLE financial_transactions (
    id BIGSERIAL PRIMARY KEY,
    transaction_no VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,  -- income, expense, refund
    category VARCHAR(50),
    amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    reference_id VARCHAR(50),  -- 关联的订单号/账单号
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 对账记录表
CREATE TABLE reconciliation_records (
    id BIGSERIAL PRIMARY KEY,
    reconcile_date DATE NOT NULL,
    channel VARCHAR(20) NOT NULL,
    total_orders INT NOT NULL,
    success_orders INT NOT NULL,
    failed_orders INT NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    reconciled_amount DECIMAL(12,2) NOT NULL,
    diff_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. API接口设计

### 4.1 计费引擎API

#### 4.1.1 计费策略管理
- `POST /api/v1/billing/strategies` - 创建计费策略
- `GET /api/v1/billing/strategies` - 查询计费策略列表
- `GET /api/v1/billing/strategies/{id}` - 获取计费策略详情
- `PUT /api/v1/billing/strategies/{id}` - 更新计费策略
- `DELETE /api/v1/billing/strategies/{id}` - 删除计费策略

#### 4.1.2 账单管理
- `POST /api/v1/billing/bills` - 生成账单
- `GET /api/v1/billing/bills` - 查询账单列表
- `GET /api/v1/billing/bills/{id}` - 获取账单详情
- `PUT /api/v1/billing/bills/{id}/status` - 更新账单状态
- `GET /api/v1/billing/bills/{id}/items` - 获取账单明细

#### 4.1.3 计费计算
- `POST /api/v1/billing/calculate` - 计算费用
- `GET /api/v1/billing/rates` - 查询费率
- `POST /api/v1/billing/rates` - 创建费率

### 4.2 支付网关API

#### 4.2.1 支付订单管理
- `POST /api/v1/payment/orders` - 创建支付订单
- `GET /api/v1/payment/orders` - 查询支付订单
- `GET /api/v1/payment/orders/{order_no}` - 获取支付订单详情
- `POST /api/v1/payment/orders/{order_no}/cancel` - 取消支付订单
- `GET /api/v1/payment/orders/{order_no}/status` - 查询支付状态

#### 4.2.2 支付回调
- `POST /api/v1/payment/callback/alipay` - 支付宝回调
- `POST /api/v1/payment/callback/wechat` - 微信支付回调
- `POST /api/v1/payment/callback/unionpay` - 银联回调

### 4.3 发票管理API

#### 4.3.1 发票管理
- `POST /api/v1/invoices` - 创建发票
- `GET /api/v1/invoices` - 查询发票列表
- `GET /api/v1/invoices/{id}` - 获取发票详情
- `PUT /api/v1/invoices/{id}` - 更新发票信息
- `DELETE /api/v1/invoices/{id}` - 删除发票
- `POST /api/v1/invoices/{id}/issue` - 开具发票
- `GET /api/v1/invoices/{id}/pdf` - 获取发票PDF

### 4.4 财务管理API

#### 4.4.1 报表管理
- `GET /api/v1/financial/reports/daily` - 日报表
- `GET /api/v1/financial/reports/monthly` - 月报表
- `GET /api/v1/financial/reports/income` - 收入分析
- `GET /api/v1/financial/reports/channel` - 渠道分析

#### 4.4.2 对账管理
- `POST /api/v1/financial/reconcile` - 执行对账
- `GET /api/v1/financial/reconcile/records` - 查询对账记录
- `GET /api/v1/financial/reconcile/records/{id}` - 获取对账详情

#### 4.4.3 财务流水
- `GET /api/v1/financial/transactions` - 查询财务流水
- `POST /api/v1/financial/transactions` - 记录财务流水

## 5. 安全设计

### 5.1 数据安全
- 敏感信息加密存储（支付密钥、API密钥）
- 支付签名验证
- HTTPS传输加密
- SQL注入防护（使用ORM参数化查询）

### 5.2 业务安全
- 重复支付检测
- 支付金额校验
- 订单状态机控制
- 幂等性设计

### 5.3 接口安全
- API Key认证
- Token认证
- 接口访问频率限制
- IP白名单

## 6. 性能优化

### 6.1 缓存策略
- Redis缓存计费策略
- Redis缓存支付状态
- 计算结果缓存

### 6.2 异步处理
- 支付回调异步处理
- 发票生成异步处理
- 报表生成异步处理

### 6.3 数据库优化
- 合理索引设计
- 分表分库（按时间/客户ID）
- 读写分离

## 7. 监控与日志

### 7.1 监控指标
- 支付成功率
- 支计费响应时间
- 错误率
- 系统可用性

### 7.2 日志记录
- 支付流水日志
- 计费计算日志
- 异常错误日志
- 操作审计日志

## 8. 部署方案

### 8.1 部署架构
- API服务: FastAPI + Gunicorn + Nginx
- 数据库: PostgreSQL主从复制
- 缓存: Redis哨兵模式
- 消息队列: Redis Pub/Sub

### 8.2 环境配置
- 开发环境
- 测试环境
- 生产环境

## 9. 测试策略

### 9.1 单元测试
- 核心业务逻辑测试
- 工具函数测试
- 数据模型测试

### 9.2 集成测试
- API接口测试
- 数据库集成测试
- 外部支付接口Mock测试

### 9.3 性能测试
- 并发支付测试
- 大批量计费测试
- 报表生成性能测试

## 10. 风险与应对

### 10.1 技术风险
- 支付接口不稳定：建立重试机制和降级方案
- 并发重复支付：实现幂等性控制
- 数据一致性：使用分布式事务或补偿机制

### 10.2 业务风险
- 计费错误：建立核对机制和人工审核流程
- 发票开具失败：提供重试和人工处理通道
- 对账差异：建立异常处理和人工确认流程

## 11. 后续优化方向

- 支持更多支付渠道
- 引入机器学习优化计费策略
- 实现智能财务预警
- 开发财务可视化大屏
- 支持多币种和多语言
