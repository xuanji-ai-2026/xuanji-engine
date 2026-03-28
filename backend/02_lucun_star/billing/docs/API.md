# 计费支付模块 API 文档

## 模块概述

本模块提供完整的计费、支付、发票和财务管理功能。

### 模块组成
- **billing_engine**: 计费引擎，负责计费策略计算、费率管理、账单生成
- **payment_gateway**: 支付网关，统一支付接口，支持多种支付渠道
- **invoice_manager**: 发票管理，发票生成、开具、管理
- **financial_management**: 财务管理，财务报表、收支统计、对账

---

## 1. 计费引擎 API (billing_engine)

### 1.1 类：BillingEngine

计费引擎主类，管理计费策略和计费计算。

#### 方法

##### `register_strategy(strategy_id, billing_type, config)`

注册计费策略。

**参数：**
- `strategy_id` (int): 策略ID
- `billing_type` (BillingType): 计费类型
  - `BillingType.USAGE`: 按量计费
  - `BillingType.TIERED`: 阶梯计费
  - `BillingType.TIME`: 时间计费
  - `BillingType.PACKAGE`: 套餐计费
- `config` (dict): 策略配置

**返回：**
- `bool`: 注册成功返回True，失败返回False

**示例：**
```python
from billing_engine import BillingEngine, BillingType

engine = BillingEngine()

# 注册按量计费策略
config = {
    "item_name": "API调用",
    "unit": "次",
    "unit_price": "0.10",
    "tax_rate": "6.00"
}
engine.register_strategy(1, BillingType.USAGE, config)
```

##### `calculate(strategy_id, customer_id, period_start, period_end, usage_data)`

计算计费。

**参数：**
- `strategy_id` (int): 策略ID
- `customer_id` (int): 客户ID
- `period_start` (date): 计费周期开始日期
- `period_end` (date): 计费周期结束日期
- `usage_data` (dict): 使用数据

**返回：**
- `BillingResult`: 计费结果

**示例：**
```python
result = engine.calculate(
    strategy_id=1,
    customer_id=1001,
    period_start=date(2024, 1, 1),
    period_end=date(2024, 1, 31),
    usage_data={"quantity": 1000}
)

print(f"总金额: {result.total_amount}")
```

##### `generate_bill_no()`

生成账单号。

**返回：**
- `str`: 账单号

### 1.2 类：BillManager

账单管理器，提供账单创建和汇总功能。

#### 方法

##### `create_bill(customer_id, strategy_id, period_start, period_end, usage_data)`

创建账单。

**参数：**
- `customer_id` (int): 客户ID
- `strategy_id` (int): 策略ID
- `period_start` (date): 计费周期开始日期
- `period_end` (date): 计费周期结束日期
- `usage_data` (dict): 使用数据

**返回：**
- `BillingResult`: 账单信息

##### `aggregate_bills(customer_id, bill_results)`

汇总账单。

**参数：**
- `customer_id` (int): 客户ID
- `bill_results` (list[BillingResult]): 待汇总的账单列表

**返回：**
- `BillingResult`: 汇总后的账单

---

## 2. 支付网关 API (payment_gateway)

### 2.1 类：PaymentGateway

支付网关主类，管理支付渠道和支付订单。

#### 方法

##### `register_adapter(channel, adapter)`

注册支付渠道适配器。

**参数：**
- `channel` (PaymentChannel): 支付渠道
  - `PaymentChannel.ALIPAY`: 支付宝
  - `PaymentChannel.WECHAT`: 微信支付
  - `PaymentChannel.UNIONPAY`: 银联
- `adapter` (PaymentAdapter): 支付适配器实例

**示例：**
```python
from payment_gateway import PaymentGateway, PaymentChannel, AlipayAdapter

gateway = PaymentGateway()

# 注册支付宝适配器
alipay_adapter = AlipayAdapter({
    "app_id": "your_app_id",
    "app_secret": "your_app_secret"
})
gateway.register_adapter(PaymentChannel.ALIPAY, alipay_adapter)
```

##### `create_payment(customer_id, amount, channel, **kwargs)`

创建支付订单。

**参数：**
- `customer_id` (int): 客户ID
- `amount` (Decimal): 支付金额
- `channel` (PaymentChannel): 支付渠道
- `subject` (str): 订单标题
- `body` (str): 订单描述
- `notify_url` (str): 异步通知URL
- `return_url` (str): 同步返回URL
- `bill_id` (str, optional): 关联账单ID

**返回：**
- `PaymentOrder`: 支付订单

**示例：**
```python
from decimal import Decimal

order = gateway.create_payment(
    customer_id=1001,
    amount=Decimal("100.00"),
    channel=PaymentChannel.ALIPAY,
    subject="云服务费用",
    notify_url="https://example.com/notify"
)

print(f"支付URL: {order.payment_url}")
print(f"订单号: {order.order_no}")
```

##### `query_payment(order_no)`

查询支付状态。

**参数：**
- `order_no` (str): 订单号

**返回：**
- `PaymentResult`: 支付结果

##### `handle_callback(channel, callback_data, signature)`

处理支付回调。

**参数：**
- `channel` (PaymentChannel): 支付渠道
- `callback_data` (dict): 回调数据
- `signature` (str, optional): 签名

**返回：**
- `PaymentCallback`: 回调信息

##### `cancel_payment(order_no)`

取消支付。

**参数：**
- `order_no` (str): 订单号

**返回：**
- `bool`: 取消成功返回True

##### `get_order(order_no)`

获取支付订单。

**参数：**
- `order_no` (str): 订单号

**返回：**
- `PaymentOrder`: 支付订单

---

## 3. 发票管理 API (invoice_manager)

### 3.1 类：InvoiceManager

发票管理器，提供发票创建、开具、作废等功能。

#### 方法

##### `create_invoice(customer_id, bill_id, type, title, tax_no, items, **kwargs)`

创建发票。

**参数：**
- `customer_id` (int): 客户ID
- `bill_id` (str): 关联账单ID
- `type` (InvoiceType): 发票类型
  - `InvoiceType.NORMAL`: 普通发票
  - `InvoiceType.VAT_SPECIAL`: 增值税专用发票
  - `InvoiceType.ELECTRONIC`: 电子发票
  - `InvoiceType.PAPER`: 纸质发票
- `title` (str): 发票抬头
- `tax_no` (str): 税号
- `items` (list[InvoiceItem]): 发票明细
- `tax_rate` (Decimal): 税率
- `address` (str): 地址
- `phone` (str): 电话
- `bank_name` (str): 银行名称
- `bank_account` (str): 银行账号

**返回：**
- `InvoiceInfo`: 发票信息

**示例：**
```python
from invoice_manager import InvoiceManager, InvoiceType, InvoiceItem
from decimal import Decimal

manager = InvoiceManager()

items = [
    InvoiceItem(
        item_name="云服务器",
        item_code="CLOUD-001",
        quantity=Decimal("1"),
        unit="台",
        unit_price=Decimal("1000.00"),
        amount=Decimal("1000.00")
    )
]

invoice = manager.create_invoice(
    customer_id=1001,
    bill_id="BILL001",
    type=InvoiceType.ELECTRONIC,
    title="测试公司",
    tax_no="91110000MA00000000",
    items=items,
    tax_rate=Decimal("6.00")
)
```

##### `issue_invoice(invoice_no)`

开具发票。

**参数：**
- `invoice_no` (str): 发票号

**返回：**
- `bool`: 开具成功返回True

##### `cancel_invoice(invoice_no)`

作废发票。

**参数：**
- `invoice_no` (str): 发票号

**返回：**
- `bool`: 作废成功返回True

##### `get_invoice(invoice_no)`

获取发票信息。

**参数：**
- `invoice_no` (str): 发票号

**返回：**
- `InvoiceInfo`: 发票信息

##### `query_invoice_status(invoice_no)`

查询发票状态。

**参数：**
- `invoice_no` (str): 发票号

**返回：**
- `str`: 发票状态

##### `generate_invoice_html(invoice_no)`

生成发票HTML。

**参数：**
- `invoice_no` (str): 发票号

**返回：**
- `str`: 发票HTML

##### `list_invoices(customer_id=None, status=None, start_date=None, end_date=None, limit=100)`

查询发票列表。

**参数：**
- `customer_id` (int, optional): 客户ID
- `status` (InvoiceStatus, optional): 发票状态
- `start_date` (date, optional): 开始日期
- `end_date` (date, optional): 结束日期
- `limit` (int): 返回数量限制

**返回：**
- `list[InvoiceInfo]`: 发票列表

##### `generate_invoice_from_bill(bill_id, customer_id, title, tax_no, bill_items, tax_rate)`

从账单生成发票。

**参数：**
- `bill_id` (str): 账单ID
- `customer_id` (int): 客户ID
- `title` (str): 发票抬头
- `tax_no` (str): 税号
- `bill_items` (list[dict]): 账单明细
- `tax_rate` (Decimal): 税率

**返回：**
- `InvoiceInfo`: 发票信息

---

## 4. 财务管理 API (financial_management)

### 4.1 类：FinancialManager

财务管理器主类，提供财务报表和对账功能。

#### 方法

##### `record_transaction(type, amount, **kwargs)`

记录财务流水。

**参数：**
- `type` (TransactionType): 交易类型
  - `TransactionType.INCOME`: 收入
  - `TransactionType.EXPENSE`: 支出
  - `TransactionType.REFUND`: 退款
- `amount` (Decimal): 金额
- `category` (str): 分类
- `description` (str): 描述
- `reference_id` (str, optional): 关联ID
- `channel` (str, optional): 支付渠道

**返回：**
- `FinancialTransaction`: 财务流水

**示例：**
```python
from financial_management import FinancialManager, TransactionType
from decimal import Decimal

manager = FinancialManager()

# 记录收入
transaction = manager.record_transaction(
    type=TransactionType.INCOME,
    amount=Decimal("1000.00"),
    category="服务收入",
    description="云服务费用",
    reference_id="ORDER001",
    channel="alipay"
)
```

########## `get_transactions(type=None, start_date=None, end_date=None, channel=None, reference_id=None, limit=100)`

查询财务流水。

**参数：**
- `type` (TransactionType, optional): 交易类型
- `start_date` (date, optional): 开始日期
- `end_date` (date, optional): 结束日期
- `channel` (str, optional): 支付渠道
- `reference_id` (str, optional): 关联ID
- `limit` (int): 返回数量限制

**返回：**
- `list[FinancialTransaction]`: 财务流水列表

##### `generate_daily_report(report_date)`

生成日报表。

**参数：**
- `report_date` (date): 报表日期

**返回：**
- `DailyReport`: 日报表

##### `generate_monthly_report(year, month)`

生成月报表。

**参数：**
- `year` (int): 年份
- `month` (int): 月份

**返回：**
- `MonthlyReport`: 月报表

##### `generate_income_report(start_date, end_date)`

生成收入分析报表。

**参数：**
- `start_date` (date): 开始日期
- `end_date` (date): 结束日期

**返回：**
- `dict`: 收入分析报表

##### `generate_channel_report(channel, start_date, end_date)`

生成渠道分析报表。

**参数：**
- `channel` (str): 支付渠道
- `start_date` (date): 开始日期
- `end_date` (date): 结束日期

**返回：**
- `dict`: 渠道分析报表

##### `reconcile(local_orders, remote_orders, channel, reconcile_date=None)`

执行对账。

**参数：**
- `local_orders` (list[dict]): 本地订单列表
- `remote_orders` (list[dict]): 远程订单列表
- `channel` (str): 支付渠道
- `reconcile_date` (date, optional): 对账日期

**返回：**
- `ReconciliationRecord`: 对账记录

**示例：**
```python
local_orders = [
    {"order_no": "ORDER001", "amount": "100.00"},
    {"order_no": "ORDER002", "amount": "200.00"}
]

remote_orders = [
    {"order_no": "ORDER001", "amount": "100.00"},
    {"order_no": "ORDER002", "amount": "200.00"}
]

record = manager.reconcile(
    local_orders=local_orders,
    remote_orders=remote_orders,
    channel="alipay"
)

print(f"对账状态: {record.status}")
print(f"成功订单数: {record.success_orders}")
print(f"差异金额: {record.diff_amount}")
```

##### `get_reconciliation_records(channel=None, start_date=None, end_date=None, limit=100)`

查询对账记录。

**参数：**
- `channel` (str, optional): 支付渠道
- `start_date` (date, optional): 开始日期
- `end_date` (date, optional): 结束日期
- `limit` (int): 返回数量限制

**返回：**
- `list[ReconciliationRecord]`: 对账记录列表

##### `get_summary(start_date=None, end_date=None)`

获取财务摘要。

**参数：**
- `start_date` (date, optional): 开始日期
- `end_date` (date, optional): 结束日期

**返回：**
- `dict`: 财务摘要

---

## 数据模型

### BillingResult
计费结果
- `customer_id` (int): 客户ID
- `strategy_id` (int): 策略ID
- `period_start` (date): 计费周期开始日期
- `period_end` (date): 计费周期结束日期
- `items` (list[BillingItem]): 计费明细
- `subtotal` (Decimal): 小计金额
- `tax_rate` (Decimal): 税率
- `tax_amount` (Decimal): 税额
- `discount` (Decimal): 折扣
- `total_amount` (Decimal): 总金额

### BillingItem
计费明细项
- `item_id` (str): 项目ID
- `item_name` (str): 项目名称
- `quantity` (Decimal): 数量
- `unit` (str): 单位
- `unit_price` (Decimal): 单价
- `amount` (Decimal): 金额

### PaymentOrder
支付订单
- `order_no` (str): 订单号
- `bill_id` (str, optional):账单ID
- `customer_id` (int): 客户ID
- `amount` (Decimal): 金额
- `currency` (str): 币种
- `channel` (PaymentChannel): 支付渠道
- `status` (PaymentStatus): 支付状态
- `payment_url` (str, optional): 支付URL
- `transaction_id` (str, optional): 交易ID

### InvoiceInfo
发票信息
- `invoice_no` (str): 发票号
- `bill_id` (str, optional): 账单ID
- `customer_id` (int): 客户ID
- `type` (InvoiceType): 发票类型
- `status` (InvoiceStatus): 发票状态
- `title` (str): 发票抬头
- `tax_no` (str): 税号
- `items` (list[InvoiceItem]): 发票明细
- `amount` (Decimal): 不含税金额
- `tax_rate` (Decimal): 税率
- `tax_amount` (Decimal): 税额
- `total_amount` (Decimal): 含税金额

### FinancialTransaction
财务流水
- `transaction_no` (str): 流水号
- `type` (TransactionType): 交易类型
- `category` (str): 分类
- `amount` (Decimal): 金额
- `description` (str): 描述
- `reference_id` (str, optional): 关联ID
- `channel` (str, optional): 支付渠道

---

## 错误处理

所有API方法都可能抛出以下异常：

- `ValueError`: 参数验证失败
- `KeyError`: 必要的配置或数据缺失
- `RuntimeError`: 运行时错误

建议在调用API时使用try-except进行错误处理。

```python
try:
    result = engine.calculate(
        strategy_id=1,
        customer_id=1001,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        usage_data={"quantity": 1000}
    )
except ValueError as e:
    print(f"参数错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")
```

---

## 最佳实践

1. **计费策略配置**
   - 为不同服务类型配置不同的计费策略
   - 使用配置文件管理计费策略，便于调整

2. **支付安全**
   - 验证所有支付回调的签名
   - 实现幂等性，防止重复处理

3. **发票管理**
   - 在支付成功后自动创建发票草稿
   - 定期批量开具发票

4. **财务对账**
   - 每日执行对账，及时发现差异
   - 保存对账记录，便于审计

5. **性能优化**
   - 使用缓存减少重复计算
   - 批量处理财务流水

---

## 示例：完整流程

```python
from datetime import date
from decimal import Decimal
from billing_engine import BillingEngine, BillManager, BillingType
from payment_gateway import PaymentGateway, PaymentChannel, AlipayAdapter
from invoice_manager import InvoiceManager, InvoiceType, InvoiceItem
from financial_management import FinancialManager, TransactionType

# 初始化各模块
billing_engine = BillingEngine()
bill_manager = BillManager(billing_engine)
payment_gateway = PaymentGateway()
invoice_manager = InvoiceManager()
financial_manager = FinancialManager()

# 注册计费策略
billing_engine.register_strategy(1, BillingType.USAGE, {
    "item_name": "云服务",
    "unit": "次",
    "unit_price": "0.10",
    "tax_rate": "6.00"
})

# 注册支付渠道
payment_gateway.register_adapter(
    PaymentChannel.ALIPAY,
    AlipayAdapter({"app_id": "xxx", "app_secret": "xxx"})
)

# 1. 生成账单
bill = bill_manager.create_bill(
    customer_id=1001,
    strategy_id=1,
    period_start=date(2024, 1, 1),
    period_end=date(2024, 1, 31),
    usage_data={"quantity": 1000}
)

print(f"账单金额: {bill.total_amount}")

# 2. 创建支付
payment_order = payment_gateway.create_payment(
    customer_id=1001,
    amount=bill.total_amount,
    channel=PaymentChannel.ALIPAY,
    subject="云服务费用",
    bill_id=bill.bill_no
)

print(f"支付URL: {payment_order.payment_url}")

# 3. 模拟支付成功后处理
# ... (用户完成支付，系统收到回调)

# 4. 创建发票
invoice_items = [
    InvoiceItem(
        item_name=item.item_name,
        quantity=item.quantity,
        unit=item.unit,
        unit_price=item.unit_price,
        amount=item.amount
    )
    for item in bill.items
]

invoice = invoice_manager.create_invoice(
    customer_id=1001,
    bill_id=bill.bill_no,
    type=InvoiceType.ELECTRONIC,
    title="测试公司",
    tax_no="91110000MA00000000",
    items=invoice_items,
    tax_rate=Decimal("6.00")
)

# 5. 开具发票
invoice_manager.issue_invoice(invoice.invoice_no)

# 6. 记录财务流水
financial_manager.record_transaction(
    type=TransactionType.INCOME,
    amount=bill.total_amount,
    category="服务收入",
    reference_id=payment_order.order_no,
    channel="alipay"
)

# 7. 生成报表
daily_report = financial_manager.generate_daily_report(date.today())
print(f"今日收入: {daily_report.income_amount}")
```

---

## 技术支持

如有问题或建议，请联系开发团队。
