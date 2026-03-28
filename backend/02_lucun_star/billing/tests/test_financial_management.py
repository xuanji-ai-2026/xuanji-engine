"""
财务管理单元测试
"""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_management.manager import (
    FinancialManager,
    TransactionType,
    ReconciliationStatus,
    FinancialTransaction,
    ReconciliationRecord,
    DailyReport,
    MonthlyReport
)


class TestFinancialManager:
    """测试财务管理器"""
    
    def setup_method(self):
        """设置测试环境"""
        self.manager = FinancialManager()
    
    def test_record_income_transaction(self):
        """测试记录收入流水"""
        transaction = self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            description="云服务费用",
            reference_id="ORDER001",
            channel="alipay"
        )
        
        assert transaction is not None
        assert transaction.type == TransactionType.INCOME
        assert transaction.amount == Decimal("1000.00")
        assert transaction.category == "服务收入"
        assert transaction.reference_id == "ORDER001"
        assert transaction.channel == "alipay"
        assert transaction in self.manager.transactions
    
    def test_record_expense_transaction(self):
        """测试记录支出流水"""
        transaction = self.manager.record_transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("500.00"),
            category="服务器成本",
            description="云服务器采购",
            reference_id="PURCHASE001"
        )
        
        assert transaction is not None
        assert transaction.type == TransactionType.EXPENSE
        assert transaction.amount == Decimal("500.00")
        assert transaction.category == "服务器成本"
    
    def test_record_refund_transaction(self):
        """测试记录退款流水"""
        transaction = self.manager.record_transaction(
            type=TransactionType.REFUND,
            amount=Decimal("100.00"),
            category="退款",
            description="订单退款",
            reference_id="ORDER001",
            channel="alipay"
        )
        
        assert transaction is not None
        assert transaction.type == TransactionType.REFUND
        assert transaction.amount == Decimal("100.00")
    
    def test_get_transactions_by_type(self):
        """测试按类型查询流水"""
        # 创建多个流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            reference_id="ORDER001",
            channel="alipay"
        )
        
        self.manager.record_transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("500.00"),
            category="服务器成本",
            reference_id="PURCHASE001"
        )
        
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("2000.00"),
            category="服务收入",
            reference_id="ORDER002",
            channel="wechat"
        )
        
        # 查询收入流水
        income_transactions = self.manager.get_transactions(type=TransactionType.INCOME)
        
        assert len(income_transactions) == 2
        assert all(t.type == TransactionType.INCOME for t in income_transactions)
    
    def test_get_transactions_by_date_range(self):
        """测试按日期范围查询流水"""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # 创建今天的流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入"
        )
        
        # 查询今天的流水
        today_transactions = self.manager.get_transactions(
            start_date=today,
            end_date=today
        )
        
        assert len(today_transactions) == 1
        
        # 查询昨天的流水
        yesterday_transactions = self.manager.get_transactions(
            start_date=yesterday,
            end_date=yesterday
        )
        
        assert len(yesterday_transactions) == 0
    
    def test_get_transactions_by_channel(self):
        """测试按渠道查询流水"""
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            channel="alipay"
        )
        
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("2000.00"),
            category="服务收入",
            channel="wechat"
        )
        
        # 查询支付宝渠道流水
        alipay_transactions = self.manager.get_transactions(channel="alipay")
        
        assert len(alipay_transactions) == 1
        assert alipay_transactions[0].channel == "alipay"
    
    def test_get_transactions_by_reference_id(self):
        """测试按关联ID查询流水"""
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            reference_id="ORDER001",
            channel="alipay"
        )
        
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("2000.00"),
            category="服务收入",
            reference_id="ORDER002",
            channel="wechat"
        )
        
        # 查询指定订单的流水
        order_transactions = self.manager.get_transactions(reference_id="ORDER001")
        
        assert len(order_transactions) == 1
        assert order_transactions[0].reference_id == "ORDER001"
    
    def test_generate_daily_report(self):
        """测试生成日报表"""
        today = date.today()
        
        # 创建今天的流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            channel="alipay"
        )
        
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("500.00"),
            category="服务收入",
            channel="wechat"
        )
        
        self.manager.record_transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("200.00"),
            category="服务器成本"
        )
        
        # 生成日报表
        report = self.manager.generate_daily_report(today)
        
        assert report.report_date == today
        assert report.income_amount == Decimal("1500.00")
        assert report.expense_amount == Decimal("200.00")
        assert report.net_amount == Decimal("1300.00")
        assert report.transaction_count == 3
        assert "alipay" in report.channel_breakdown
        assert "wechat" in report.channel_breakdown
    
    def test_generate_monthly_report(self):
        """测试生成月报表"""
        today = date.today()
        year = today.year
        month = today.month
        
        # 创建本月的流水
        for i in range(30):
            self.manager.record_transaction(
                type=TransactionType.INCOME,
                amount=Decimal("100.00"),
                category="服务收入",
                channel="alipay"
            )
        
        # 生成月报表
        report = self.manager.generate_monthly_report(year, month)
        
        assert report.year == year
        assert report.month == month
        assert report.income_amount == Decimal("3000.00")
        assert report.transaction_count == 30
        assert len(report.daily_trend) > 0
    
    def test_generate_income_report(self):
        """测试生成收入分析报表"""
        today = date.today()
        
        # 创建流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            channel="alipay"
        )
        
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("500.00"),
            category="产品销售",
            channel="wechat"
        )
        
        # 生成收入分析报表
        report = self.manager.generate_income_report(
            start_date=today,
            end_date=today
        )
        
        assert report["total_income"] == "1500.00"
        assert report["transaction_count"] == 2
        assert "alipay" in report["by_channel"]
        assert "wechat" in report["by_channel"]
        assert "服务收入" in report["by_category"]
        assert "产品销售" in report["by_category"]
    
    def test_generate_channel_report(self):
        """测试生成渠道分析报表"""
        today = date.today()
        
        # 创建支付宝流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入",
            channel="alipay",
            reference_id="ORDER001"
        )
        
        self.manager.record_transaction(
            type=TransactionType.REFUND,
            amount=Decimal("50.00"),
            category="退款",
            channel="alipay",
            reference_id="ORDER002"
        )
        
        # 生成支付宝渠道报表
        report = self.manager.generate_channel_report(
            channel="alipay",
            start_date=today,
            end_date=today
        )
        
        assert report["channel"] == "alipay"
        assert report["total_amount"] == "1050.00"
        assert report["transaction_count"] == 2
        assert report["success_count"] == 1
        assert report["refund_count"] == 1
        assert report["success_rate"] == "50.00%"
    
    def test_reconcile_success(self):
        """测试对账成功"""
        local_orders = [
            {"order_no": "ORDER001", "amount": "100.00"},
            {"order_no": "ORDER002", "amount": "200.00"}
        ]
        
        remote_orders = [
            {"order_no": "ORDER001", "amount": "100.00"},
            {"order_no": "ORDER002", "amount": "200.00"}
        ]
        
        record = self.manager.reconcile(
            local_orders=local_orders,
            remote_orders=remote_orders,
            channel="alipay"
        )
        
        assert record is not None
        assert record.channel == "alipay"
        assert record.total_orders == 2
        assert record.success_orders == 2
        assert record.failed_orders == 0
        assert record.total_amount == Decimal("300.00")
        assert record.reconciled_amount == Decimal("300.00")
        assert record.diff_amount == Decimal("0.00")
        assert record.status == ReconciliationStatus.SUCCESS
    
    def test_reconcile_with_diff(self):
        """测试对账有差异"""
        local_orders = [
            {"order_no": "ORDER001", "amount": "100.00"},
            {"order_no": "ORDER002", "amount": "200.00"}
        ]
        
        remote_orders = [
            {"order_no": "ORDER001", "amount": "100.00"},
            {"order_no": "ORDER002", "amount": "250.00"}  # 金额不一致
        ]
        
        record = self.manager.reconcile(
            local_orders=local_orders,
            remote_orders=remote_orders,
            channel="wechat"
        )
        
        assert record is not None
        assert record.total_orders == 2
        assert record.success_orders == 1
        assert record.failed_orders == 1
        assert record.diff_amount == Decimal("50.00")
        assert record.status == ReconciliationStatus.FAILED
        assert len(record.details["diff_orders"]) == 1
    
    def test_reconcile_with_missing_orders(self):
        """测试对账发现缺失订单"""
        local_orders = [
            {"order_no": "ORDER001", "amount": "100.00"},
            {"order_no": "ORDER002", "amount": "200.00"}
        ]
        
        remote_orders = [
            {"order_no": "ORDER001", "amount": "100.00"}
            # ORDER002 缺失
        ]
        
        record = self.manager.reconcile(
            local_orders=local_orders,
            remote_orders=remote_orders,
            channel="alipay"
        )
        
        assert record is not None
        assert record.total_orders == 2
        assert record.success_orders == 1
        assert record.failed_orders == 1
        assert record.status == ReconciliationStatus.FAILED
        assert len(record.details["missing_orders"]) == 1
        assert "ORDER002" in record.details["missing_orders"]
    
    def test_get_reconciliation_records(self):
        """测试查询对账记录"""
        local_orders = [{"order_no": "ORDER001", "amount": "100.00"}]
        remote_orders = [{"order_no": "ORDER001", "amount": "100.00"}]
        
        self.manager.reconcile(
            local_orders=local_orders,
            remote_orders=remote_orders,
            channel="alipay"
        )
        
        records = self.manager.get_reconciliation_records()
        
        assert len(records) == 1
        assert records[0].channel == "alipay"
    
    def test_get_reconciliation_records_by_channel(self):
        """测试按渠道查询对账记录"""
        local_orders1 = [{"order_no": "ORDER001", "amount": "100.00"}]
        remote_orders1 = [{"order_no": "ORDER001", "amount": "100.00"}]
        
        local_orders2 = [{"order_no": "ORDER002", "amount": "200.00"}]
        remote_orders2 = [{"order_no": "ORDER002", "amount": "200.00"}]
        
        self.manager.reconcile(
            local_orders=local_orders1,
            remote_orders=remote_orders1,
            channel="alipay"
        )
        
        self.manager.reconcile(
            local_orders=local_orders2,
            remote_orders=remote_orders2,
            channel="wechat"
        )
        
        # 查询支付宝对账记录
        alipay_records = self.manager.get_reconciliation_records(channel="alipay")
        
        assert len(alipay_records) == 1
        assert alipay_records[0].channel == "alipay"
    
    def test_get_summary(self):
        """测试获取财务摘要"""
        # 创建流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入"
        )
        
        self.manager.record_transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("200.00"),
            category="服务器成本"
        )
        
        self.manager.record_transaction(
            type=TransactionType.REFUND,
            amount=Decimal("50.00"),
            category="退款"
        )
        
        summary = self.manager.get_summary()
        
        assert summary["total_income"] == "1000.00"
        assert summary["total_expense"] == "200.00"
        assert summary["total_refund"] == "50.00"
        assert summary["net_amount"] == "750.00"  # 1000 - 200 - 50
        assert summary["transaction_count"] == 3
    
    def test_get_summary_with_date_range(self):
        """测试按日期范围获取财务摘要"""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # 创建今天的流水
        self.manager.record_transaction(
            type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category="服务收入"
        )
        
        # 查询今天的摘要
        summary = self.manager.get_summary(
            start_date=today,
            end_date=today
        )
        
        assert summary["transaction_count"] == 1
        assert summary["total_income"] == "1000.00"
        
        # 查询昨天的摘要
        summary_yesterday = self.manager.get_summary(
            start_date=yesterday,
            end_date=yesterday
        )
        
        assert summary_yesterday["transaction_count"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
