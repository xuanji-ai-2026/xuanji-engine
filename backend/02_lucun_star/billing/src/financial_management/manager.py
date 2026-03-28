"""
财务管理核心模块
负责财务报表、收支统计、对账
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
import json


class TransactionType(Enum):
    """交易类型"""
    INCOME = "income"  # 收入
    EXPENSE = "expense"  # 支出
    REFUND = "refund"  # 退款


class ReconciliationStatus(Enum):
    """对账状态"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class FinancialTransaction:
    """财务流水"""
    transaction_no: str = field(default_factory=lambda: str(uuid4()))
    type: TransactionType = TransactionType.INCOME
    category: str = ""
    amount: Decimal = Decimal("0.00")
    description: str = ""
    reference_id: Optional[str] = None  # 关联的订单号/账单号
    channel: Optional[str] = None  # 支付渠道
    currency: str = "CNY"
    tags: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ReconciliationRecord:
    """对账记录"""
    id: str = field(default_factory=lambda: str(uuid4()))
    reconcile_date: date = field(default_factory=date.today)
    channel: str = ""
    total_orders: int = 0
    success_orders: int = 0
    failed_orders: int = 0
    total_amount: Decimal = Decimal("0.00")
    reconciled_amount: Decimal = Decimal("0.00")
    diff_amount: Decimal = Decimal("0.00")
    status: ReconciliationStatus = ReconciliationStatus.PENDING
    details: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DailyReport:
    """日报表"""
    report_date: date
    income_amount: Decimal = Decimal("0.00")
    expense_amount: Decimal = Decimal("0.00")
    refund_amount: Decimal = Decimal("0.00")
    net_amount: Decimal = Decimal("0.00")
    transaction_count: int = 0
    channel_breakdown: Dict[str, Decimal] = field(default_factory=dict)
    category_breakdown: Dict[str, Decimal] = field(default_factory=dict)


@dataclass
class MonthlyReport:
    """月报表"""
    year: int = 0
    month: int = 0
    income_amount: Decimal = Decimal("0.00")
    expense_amount: Decimal = Decimal("0.00")
    refund_amount: Decimal = Decimal("0.00")
    net_amount: Decimal = Decimal("0.00")
    transaction_count: int = 0
    daily_trend: List[Dict[str, Any]] = field(default_factory=list)
    channel_breakdown: Dict[str, Decimal] = field(default_factory=dict)
    top_customers: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CustomerReport:
    """客户报表"""
    customer_id: int = 0
    customer_name: str = ""
    total_amount: Decimal = Decimal("0.00")
    payment_count: int = 0
    avg_amount: Decimal = Decimal("0.00")
    first_payment_date: Optional[date] = None
    last_payment_date: Optional[date] = None


class ReportGenerator:
    """报表生成器"""
    
    @staticmethod
    def generate_daily_report(
        transactions: List[FinancialTransaction],
        report_date: date
    ) -> DailyReport:
        """生成日报表"""
        report = DailyReport(report_date=report_date)
        
        for transaction in transactions:
            if transaction.created_at.date() != report_date:
                continue
            
            report.transaction_count += 1
            
            if transaction.type == TransactionType.INCOME:
                report.income_amount += transaction.amount
            elif transaction.type == TransactionType.EXPENSE:
                report.expense_amount += transaction.amount
            elif transaction.type == TransactionType.REFUND:
                report.refund_amount += transaction.amount
            
            # 渠道统计
            if transaction.channel:
                if transaction.channel not in report.channel_breakdown:
                    report.channel_breakdown[transaction.channel] = Decimal("0.00")
                report.channel_breakdown[transaction.channel] += transaction.amount
            
            # 分类统计
            if transaction.category:
                if transaction.category not in report.category_breakdown:
                    report.category_breakdown[transaction.category] = Decimal("0.00")
                report.category_breakdown[transaction.category] += transaction.amount
        
        report.net_amount = report.income_amount - report.expense_amount - report.refund_amount
        return report
    
    @staticmethod
    def generate_monthly_report(
        transactions: List[FinancialTransaction],
        year: int,
        month: int
    ) -> MonthlyReport:
        """生成月报表"""
        report = MonthlyReport(year=year, month=month)
        
        month_start = date(year, month, 1)
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)
        
        # 每日统计
        daily_data: Dict[date, Dict[str, Any]] = {}
        customer_data: Dict[int, Dict[str, Any]] = {}
        
        for transaction in transactions:
            transaction_date = transaction.created_at.date()
            
            if not (month_start <= transaction_date <= month_end):
                continue
            
            report.transaction_count += 1
            
            if transaction.type == TransactionType.INCOME:
                report.income_amount += transaction.amount
            elif transaction.type == TransactionType.EXPENSE:
                report.expense_amount += transaction.amount
            elif transaction.type == TransactionType.REFUND:
                report.refund_amount += transaction.amount
            
            # 渠道统计
            if transaction.channel:
                if transaction.channel not in report.channel_breakdown:
                    report.channel_breakdown[transaction.channel] = Decimal("0.00")
                report.channel_breakdown[transaction.channel] += transaction.amount
            
            # 每日趋势
            if transaction_date not in daily_data:
                daily_data[transaction_date] = {
                    "date": transaction_date.isoformat(),
                    "income": Decimal("0.00"),
                    "expense": Decimal("0.00"),
                    "refund": Decimal("0.00"),
                    "net": Decimal("0.00")
                }
            
            if transaction.type == TransactionType.INCOME:
                daily_data[transaction_date]["income"] += transaction.amount
            elif transaction.type == TransactionType.EXPENSE:
                daily_data[transaction_date]["expense"] += transaction.amount
            elif transaction.type == TransactionType.REFUND:
                daily_data[transaction_date]["refund"] += transaction.amount
            
            daily_data[transaction_date]["net"] = (
                daily_data[transaction_date]["income"] -
                daily_data[transaction_date]["expense"] -
                daily_data[transaction_date]["refund"]
            )
            
            # 客户统计（通过reference_id关联）
            if transaction.reference_id and transaction.type == TransactionType.INCOME:
                # 简化处理：使用reference_id作为客户标识
                customer_key = hash(transaction.reference_id) % 10000
                if customer_key not in customer_data:
                    customer_data[customer_key] = {
                        "customer_id": customer_key,
                        "total_amount": Decimal("0.00"),
                        "count": 0
                    }
                customer_data[customer_key]["total_amount"] += transaction.amount
                customer_data[customer_key]["count"] += 1
        
        report.net_amount = report.income_amount - report.expense_amount - report.refund_amount
        report.daily_trend = sorted(daily_data.values(), key=lambda x: x["date"])
        
        # Top客户
        sorted_customers = sorted(
            customer_data.values(),
            key=lambda x: x["total_amount"],
            reverse=True
        )[:10]
        report.top_customers = sorted_customers
        
        return report
    
    @staticmethod
    def generate_income_report(
        transactions: List[FinancialTransaction],
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """生成收入分析报表"""
        income_transactions = [
            t for t in transactions
            if t.type == TransactionType.INCOME
            and start_date <= t.created_at.date() <= end_date
        ]
        
        total_income = sum(t.amount for t in income_transactions)
        
        # 按渠道分组
        by_channel: Dict[str, Decimal] = {}
        for transaction in income_transactions:
            channel = transaction.channel or "unknown"
            if channel not in by_channel:
                by_channel[channel] = Decimal("0.00")
            by_channel[channel] += transaction.amount
        
        # 按分类分组
        by_category: Dict[str, Decimal] = {}
        for transaction in income_transactions:
            category = transaction.category or "unknown"
            if category not in by_category:
                by_category[category] = Decimal("0.00")
            by_category[category] += transaction.amount
        
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_income": str(total_income),
            "transaction_count": len(income_transactions),
            "by_channel": {k: str(v) for k, v in by_channel.items()},
            "by_category": {k: str(v) for k, v in by_category.items()}
        }
    
    @staticmethod
    def generate_channel_report(
        transactions: List[FinancialTransaction],
        channel: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """生成渠道分析报表"""
        channel_transactions = [
            t for t in transactions
            if t.channel == channel
            and start_date <= t.created_at.date() <= end_date
        ]
        
        total_amount = sum(t.amount for t in channel_transactions)
        success_count = sum(
            1 for t in channel_transactions
            if t.type == TransactionType.INCOME
        )
        refund_count = sum(
            1 for t in channel_transactions
            if t.type == TransactionType.REFUND
        )
        
        return {
            "channel": channel,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_amount": str(total_amount),
            "transaction_count": len(channel_transactions),
            "success_count": success_count,
            "refund_count": refund_count,
            "success_rate": f"{(success_count / len(channel_transactions) * 100):.2f}%" if channel_transactions else "0%"
        }


class ReconciliationService:
    """对账服务"""
    
    def __init__(self):
        self.records: List[ReconciliationRecord] = []
    
    def reconcile(
        self,
        local_orders: List[Dict[str, Any]],
        remote_orders: List[Dict[str, Any]],
        channel: str,
        reconcile_date: date
    ) -> ReconciliationRecord:
        """执行对账"""
        record = ReconciliationRecord(
            reconcile_date=reconcile_date,
            channel=channel,
            total_orders=len(local_orders),
            details={}
        )
        
        # 计算本地总金额
        local_total = sum(
            Decimal(str(order.get("amount", "0")))
            for order in local_orders
        )
        
        # 计算远程总金额
        remote_total = sum(
            Decimal(str(order.get("amount", "0")))
            for order in remote_orders
        )
        
        record.total_amount = local_total
        record.reconciled_amount = remote_total
        record.diff_amount = remote_total - local_total
        
        # 比对订单
        local_order_map = {
            order.get("order_no"): order
            for order in local_orders
        }
        remote_order_map = {
            order.get("order_no"): order
            for order in remote_orders
        }
        
        # 找出缺失和差异的订单
        missing_orders = []
        diff_orders = []
        
        for order_no, local_order in local_order_map.items():
            remote_order = remote_order_map.get(order_no)
            
            if not remote_order:
                missing_orders.append(order_no)
                record.failed_orders += 1
            else:
                local_amount = Decimal(str(local_order.get("amount", "0")))
                remote_amount = Decimal(str(remote_order.get("amount", "0")))
                
                if local_amount != remote_amount:
                    diff_orders.append({
                        "order_no": order_no,
                        "local_amount": str(local_amount),
                        "remote_amount": str(remote_amount),
                        "diff": str(remote_amount - local_amount)
                    })
                    record.failed_orders += 1
                else:
                    record.success_orders += 1
        
        record.details = {
            "missing_orders": missing_orders,
            "diff_orders": diff_orders
        }
        
        # 判断对账状态
        if record.diff_amount == 0 and record.failed_orders == 0:
            record.status = ReconciliationStatus.SUCCESS
        elif record.failed_orders == 0:
            record.status = ReconciliationStatus.PARTIAL
        else:
            record.status = ReconciliationStatus.FAILED
        
        self.records.append(record)
        return record
    
    def get_reconciliation_records(
        self,
        channel: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> List[ReconciliationRecord]:
        """查询对账记录"""
        result = []
        
        for record in self.records:
            if channel and record.channel != channel:
                continue
            
            if start_date and record.reconcile_date < start_date:
                continue
            
            if end_date and record.reconcile_date > end_date:
                continue
            
            result.append(record)
            
            if len(result) >= limit:
                break
        
        return sorted(
            result,
            key=lambda x: x.reconcile_date,
            reverse=True
        )


class FinancialManager:
    """财务管理器主类"""
    
    def __init__(self):
        self.transactions: List[FinancialTransaction] = []
        self.reconciliation_service = ReconciliationService()
        self.report_generator = ReportGenerator()
    
    def record_transaction(
        self,
        type: TransactionType,
        amount: Decimal,
        category: str = "",
        description: str = "",
        reference_id: Optional[str] = None,
        channel: Optional[str] = None,
        **kwargs
    ) -> FinancialTransaction:
        """记录财务流水"""
        transaction = FinancialTransaction(
            type=type,
            amount=amount,
            category=category,
            description=description,
            reference_id=reference_id,
            channel=channel,
            **kwargs
        )
        
        self.transactions.append(transaction)
        return transaction
    
    def get_transactions(
        self,
        type: Optional[TransactionType] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        channel: Optional[str] = None,
        reference_id: Optional[str] = None,
        limit: int = 100
    ) -> List[FinancialTransaction]:
        """查询财务流水"""
        result = []
        
        for transaction in self.transactions:
            if type and transaction.type != type:
                continue
            
            if start_date and transaction.created_at.date() < start_date:
                continue
            
            if end_date and transaction.created_at.date() > end_date:
                continue
            
            if channel and transaction.channel != channel:
                continue
            
            if reference_id and transaction.reference_id != reference_id:
                continue
            
            result.append(transaction)
            
            if len(result) >= limit:
                break
        
        return sorted(
            result,
            key=lambda x: x.created_at,
            reverse=True
        )
    
    def generate_daily_report(self, report_date: date) -> DailyReport:
        """生成日报表"""
        return self.report_generator.generate_daily_report(
            self.transactions,
            report_date
        )
    
    def generate_monthly_report(self, year: int, month: int) -> MonthlyReport:
        """生成月报表"""
        return self.report_generator.generate_monthly_report(
            self.transactions,
            year,
            month
        )
    
    def generate_income_report(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """生成收入分析报表"""
        return self.report_generator.generate_income_report(
            self.transactions,
            start_date,
            end_date
        )
    
    def generate_channel_report(
        self,
        channel: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """生成渠道分析报表"""
        return self.report_generator.generate_channel_report(
            self.transactions,
            channel,
            start_date,
            end_date
        )
    
    def reconcile(
        self,
        local_orders: List[Dict[str, Any]],
        remote_orders: List[Dict[str, Any]],
        channel: str,
        reconcile_date: Optional[date] = None
    ) -> ReconciliationRecord:
        """执行对账"""
        return self.reconciliation_service.reconcile(
            local_orders,
            remote_orders,
            channel,
            reconcile_date or date.today()
        )
    
    def get_reconciliation_records(self, **kwargs) -> List[ReconciliationRecord]:
        """查询对账记录"""
        return self.reconciliation_service.get_reconciliation_records(**kwargs)
    
    def get_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """获取财务摘要"""
        filtered_transactions = self.transactions
        
        if start_date or end_date:
            filtered_transactions = [
                t for t in self.transactions
                if (not start_date or t.created_at.date() >= start_date)
                and (not end_date or t.created_at.date() <= end_date)
            ]
        
        total_income = sum(
            t.amount for t in filtered_transactions
            if t.type == TransactionType.INCOME
        )
        total_expense = sum(
            t.amount for t in filtered_transactions
            if t.type == TransactionType.EXPENSE
        )
        total_refund = sum(
            t.amount for t in filtered_transactions
            if t.type == TransactionType.REFUND
        )
        
        return {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "total_income": str(total_income),
            "total_expense": str(total_expense),
            "total_refund": str(total_refund),
            "net_amount": str(total_income - total_expense - total_refund),
            "transaction_count": len(filtered_transactions)
        }
