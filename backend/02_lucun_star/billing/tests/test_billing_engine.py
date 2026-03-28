"""
计费引擎单元测试
"""

import pytest
from datetime import date, datetime
from decimal import Decimal

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from billing_engine.engine import (
    BillingEngine,
    BillingType,
    BillStatus,
    BillingItem,
    BillingResult,
    BillManager
)


class TestBillingEngine:
    """测试计费引擎"""
    
    def setup_method(self):
        """设置测试环境"""
        self.engine = BillingEngine()
    
    def test_register_usage_strategy(self):
        """测试注册按量计费策略"""
        config = {
            "item_name": "API调用",
            "unit": "次",
            "unit_price": "0.10",
            "tax_rate": "6.00"
        }
        
        result = self.engine.register_strategy(
            strategy_id=1,
            billing_type=BillingType.USAGE,
            config=config
        )
        
        assert result is True
        assert 1 in self.engine.strategies
    
    def test_register_tiered_strategy(self):
        """测试注册阶梯计费策略"""
        config = {
            "unit": "次",
            "tax_rate": "6.00",
            "tiers": [
                {"name": "基础阶梯", "start": 0, "end": 1000, "price": "0.10"},
                {"name": "高级阶梯", "start": 1001, "end": 10000, "price": "0.08"}
            ]
        }
        
        result = self.engine.register_strategy(
            strategy_id=2,
            billing_type=BillingType.TIERED,
            config=config
        )
        
        assert result is True
        assert 2 in self.engine.strategies
    
    def test_register_time_strategy(self):
        """测试注册时间计费策略"""
        config = {
            "item_name": "云服务器",
            "hourly_rate": "5.00",
            "tax_rate": "6.00"
        }
        
        result = self.engine.register_strategy(
            strategy_id=3,
            billing_type=BillingType.TIME,
            config=config
        )
        
        assert result is True
        assert 3 in self.engine.strategies
    
    def test_register_package_strategy(self):
        """测试注册套餐计费策略"""
        config = {
            "package_name": "基础套餐",
            "package_price": "100.00",
            "package_limit": "1000",
            "overage_rate": "0.15",
            "unit": "次",
            "tax_rate": "6.00"
        }
        
        result = self.engine.register_strategy(
            strategy_id=4,
            billing_type=BillingType.PACKAGE,
            config=config
        )
        
        assert result is True
        assert 4 in self.engine.strategies
    
    def test_calculate_usage_billing(self):
        """测试按量计费计算"""
        config = {
            "item_name": "API调用",
            "unit": "次",
            "unit_price": "0.10",
            "tax_rate": "6.00"
        }
        
        self.engine.register_strategy(
            strategy_id=1,
            billing_type=BillingType.USAGE,
            config=config
        )
        
        result = self.engine.calculate(
            strategy_id=1,
            customer_id=1001,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            usage_data={"quantity": 1000}
        )
        
        assert result is not None
        assert result.customer_id == 1001
        assert len(result.items) == 1
        assert result.items[0].quantity == Decimal("1000")
        assert result.items[0].unit_price == Decimal("0.10")
        assert result.items[0].amount == Decimal("100.00")
        assert result.subtotal == Decimal("100.00")
        assert result.tax_amount == Decimal("6.00")
        assert result.total_amount == Decimal("106.00")
    
    def test_calculate_tiered_billing(self):
        """测试阶梯计费计算"""
        config = {
            "unit": "次",
            "tax_rate": "6.00",
            "tiers": [
                {"name": "基础阶梯", "start": 0, "end": 1000, "price": "0.10"},
                {"name": "高级阶梯", "start": 1001, "end": 10000, "price": "0.08"}
            ]
        }
        
        self.engine.register_strategy(
            strategy_id=2,
            billing_type=BillingType.TIERED,
            config=config
        )
        
        # 测试跨阶梯计费
        result = self.engine.calculate(
            strategy_id=2,
            customer_id=1001,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            usage_data={"quantity": 1500}
        )
        
        assert result is not None
        assert len(result.items) == 2
        # 1001个在第一阶梯 (0-1000)，499个在第二阶梯 (1001-10000)
        # 1001 * 0.10 + 499 * 0.08 = 100.1 + 39.92 = 140.02
        assert result.subtotal == Decimal("140.02")
    
    def test_calculate_time_billing(self):
        """测试时间计费计算"""
        config = {
            "item_name": "云服务器",
            "hourly_rate": "5.00",
            "tax_rate": "6.00"
        }
        
        self.engine.register_strategy(
            strategy_id=3,
            billing_type=BillingType.TIME,
            config=config
        )
        
        result = self.engine.calculate(
            strategy_id=3,
            customer_id=1001,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            usage_data={"hours": 24}
        )
        
        assert result is not None
        assert result.items[0].quantity == Decimal("24")
        assert result.items[0].unit_price == Decimal("5.00")
        assert result.items[0].amount == Decimal("120.00")
    
    def test_calculate_package_billing(self):
        """测试套餐计费计算"""
        config = {
            "package_name": "基础套餐",
            "package_price": "100.00",
            "package_limit": "1000",
            "overage_rate": "0.15",
            "unit": "次",
            "tax_rate": "6.00"
        }
        
        self.engine.register_strategy(
            strategy_id=4,
            billing_type=BillingType.PACKAGE,
            config=config
        )
        
        # 测试超量计费
        result = self.engine.calculate(
            strategy_id=4,
            customer_id=1001,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            usage_data={"quantity": 1200}
        )
        
        assert result is not None
        assert len(result.items) == 2  # 套餐 + 超量
        assert result.items[0].amount == Decimal("100.00")  # 套餐费
        assert result.items[1].amount == Decimal("30.00")  # 超量费  * 0.15
        assert result.subtotal == Decimal("130.00")
    
    def test_generate_bill_no(self):
        """测试生成账单号"""
        bill_no = self.engine.generate_bill_no()
        
        assert bill_no.startswith("BILL")
        assert len(bill_no) > 8
    
    def test_calculate_invalid_strategy(self):
        """测试不存在的策略"""
        result = self.engine.calculate(
            strategy_id=999,
            customer_id=1001,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            usage_data={"quantity": 1000}
        )
        
        assert result is None


class TestBillManager:
    """测试账单管理器"""
    
    def setup_method(self):
        """设置测试环境"""
        self.engine = BillingEngine()
        self.manager = BillManager(self.engine)
        
        # 注册测试策略
        config = {
            "item_name": "API调用",
            "unit": "次",
            "unit_price": "0.10",
            "tax_rate": "6.00"
        }
        self.engine.register_strategy(
            strategy_id=1,
            billing_type=BillingType.USAGE,
            config=config
        )
    
    def test_create_bill(self):
        """测试创建账单"""
        result = self.manager.create_bill(
            customer_id=1001,
            strategy_id=1,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            usage_data={"quantity": 1000}
        )
        
        assert result is not None
        assert result.customer_id == 1001
        assert result.total_amount == Decimal("106.00")
    
    def test_aggregate_bills(self):
        """测试汇总账单"""
        # 创建多个账单
        bill1 = self.manager.create_bill(
            customer_id=1001,
            strategy_id=1,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 15),
            usage_data={"quantity": 500}
        )
        
        bill2 = self.manager.create_bill(
            customer_id=1001,
            strategy_id=1,
            period_start=date(2024, 1, 16),
            period_end=date(2024, 1, 31),
            usage_data={"quantity": 500}
        )
        
        aggregated = self.manager.aggregate_bills(customer_id=1001, bill_results=[bill1, bill2])
        
        assert aggregated.customer_id == 1001
        assert len(aggregated.items) == 1  # 相同项目合并
        assert aggregated.items[0].quantity == Decimal("1000")  # 500 + 500
        assert aggregated.total_amount == Decimal("106.00")  # 100*0.10 + 6%税
    
    def test_aggregate_empty_bills(self):
        """测试汇总空账单"""
        aggregated = self.manager.aggregate_bills(customer_id=1001, bill_results=[])
        
        assert aggregated.customer_id == 1001
        assert len(aggregated.items) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
