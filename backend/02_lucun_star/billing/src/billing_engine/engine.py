"""
计费引擎核心模块
负责计费策略计算、费率管理、账单生成
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class BillingType(Enum):
    """计费类型"""
    USAGE = "usage"  # 按量计费
    TIERED = "tiered"  # 阶梯计费
    TIME = "time"  # 时间计费
    PACKAGE = "package"  # 套餐计费
    CUSTOM = "custom"  # 自定义计费


class BillStatus(Enum):
    """账单状态"""
    UNPAID = "unpaid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


@dataclass
class BillingItem:
    """计费明细项"""
    item_id: str = field(default_factory=lambda: str(uuid4()))
    item_name: str = ""
    quantity: Decimal = Decimal("0")
    unit: str = ""
    unit_price: Decimal = Decimal("0.00")
    amount: Decimal = Decimal("0.00")
    description: str = ""


@dataclass
class BillingResult:
    """计费结果"""
    customer_id: int
    strategy_id: int
    period_start: date
    period_end: date
    items: List[BillingItem] = field(default_factory=list)
    subtotal: Decimal = Decimal("0.00")
    tax_rate: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    discount: Decimal = Decimal("0.00")
    total_amount: Decimal = Decimal("0.00")
    
    def calculate_total(self):
        """计算总金额"""
        self.subtotal = sum(item.amount for item in self.items)
        self.tax_amount = self.subtotal * self.tax_rate / Decimal("100")
        self.total_amount = self.subtotal + self.tax_amount - self.discount


class BillingStrategy(ABC):
    """计费策略基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    @abstractmethod
    def calculate(
        self,
        customer_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> BillingResult:
        """计算计费结果"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        pass


class UsageBillingStrategy(BillingStrategy):
    """按量计费策略"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.unit = config.get("unit", "次")
        self.unit_price = Decimal(str(config.get("unit_price", "0.00")))
    
    def calculate(
        self,
        customer_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> BillingResult:
        """按量计费"""
        quantity = Decimal(str(usage_data.get("quantity", "0")))
        
        item = BillingItem(
            item_name=self.config.get("item_name", "服务费用"),
            quantity=quantity,
            unit=self.unit,
            unit_price=self.unit_price,
            amount=quantity * self.unit_price
        )
        
        result = BillingResult(
            customer_id=customer_id,
            strategy_id=self.config.get("strategy_id", 0),
            period_start=period_start,
            period_end=period_end,
            items=[item],
            tax_rate=Decimal(str(self.config.get("tax_rate", "0.00")))
        )
        result.calculate_total()
        return result
    
    def validate_config(self) -> bool:
        """验证配置"""
        return "unit_price" in self.config and self.unit_price > 0


class TieredBillingStrategy(BillingStrategy):
    """阶梯计费策略"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.tiers = config.get("tiers", [])
    
    def calculate(
        self,
        customer_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> BillingResult:
        """阶梯计费"""
        quantity = Decimal(str(usage_data.get("quantity", "0")))
        items = []
        remaining = quantity
        
        for tier in self.tiers:
            tier_start = Decimal(str(tier.get("start", "0")))
            tier_end = Decimal(str(tier.get("end", "999999")))
            tier_price = Decimal(str(tier.get("price", "0.00")))
            
            if remaining <= 0:
                break
            
            # 计算当前阶梯的使用量（tier_start到tier_end是闭区间）
            tier_quantity = min(remaining, tier_end - tier_start + Decimal("1"))
            
            amount = tier_quantity * tier_price
            items.append(BillingItem(
                item_name=f"{tier.get('name', f'阶梯{tier_start}-{tier_end}')}",
                quantity=tier_quantity,
                unit=self.config.get("unit", "次"),
                unit_price=tier_price,
                amount=amount
            ))
            
            remaining -= tier_quantity
        
        result = BillingResult(
            customer_id=customer_id,
            strategy_id=self.config.get("strategy_id", 0),
            period_start=period_start,
            period_end=period_end,
            items=items,
            tax_rate=Decimal(str(self.config.get("tax_rate", "0.00")))
        )
        result.calculate_total()
        return result
    
    def validate_config(self) -> bool:
        """验证配置"""
        return bool(self.tiers) and all(
            "price" in tier for tier in self.tiers
        )


class TimeBillingStrategy(BillingStrategy):
    """时间计费策略"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.hourly_rate = Decimal(str(config.get("hourly_rate", "0.00")))
    
    def calculate(
        self,
        customer_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> BillingResult:
        """按时间计费"""
        hours = Decimal(str(usage_data.get("hours", "0")))
        
        item = BillingItem(
            item_name=self.config.get("item_name", "时长费用"),
            quantity=hours,
            unit="小时",
            unit_price=self.hourly_rate,
            amount=hours * self.hourly_rate
        )
        
        result = BillingResult(
            customer_id=customer_id,
            strategy_id=self.config.get("strategy_id", 0),
            period_start=period_start,
            period_end=period_end,
            items=[item],
            tax_rate=Decimal(str(self.config.get("tax_rate", "0.00")))
        )
        result.calculate_total()
        return result
    
    def validate_config(self) -> bool:
        """验证配置"""
        return self.hourly_rate > 0


class PackageBillingStrategy(BillingStrategy):
    """套餐计费策略"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.package_name = config.get("package_name", "基础套餐")
        self.package_price = Decimal(str(config.get("package_price", "0.00")))
        self.package_limit = Decimal(str(config.get("package_limit", "0")))
        self.overage_rate = Decimal(str(config.get("overage_rate", "0.00")))
    
    def calculate(
        self,
        customer_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> BillingResult:
        """套餐计费"""
        items = []
        quantity = Decimal(str(usage_data.get("quantity", "0")))
        
        # 套餐费用
        items.append(BillingItem(
            item_name=self.package_name,
            quantity=Decimal("1"),
            unit="套",
            unit_price=self.package_price,
            amount=self.package_price
        ))
        
        # 超量费用
        if quantity > self.package_limit and self.overage_rate > 0:
            overage = quantity - self.package_limit
            items.append(BillingItem(
                item_name=f"{self.package_name}超量",
                quantity=overage,
                unit=self.config.get("unit", "次"),
                unit_price=self.overage_rate,
                amount=overage * self.overage_rate
            ))
        
        result = BillingResult(
            customer_id=customer_id,
            strategy_id=self.config.get("strategy_id", 0),
            period_start=period_start,
            period_end=period_end,
            items=items,
            tax_rate=Decimal(str(self.config.get("tax_rate", "0.00")))
        )
        result.calculate_total()
        return result
    
    def validate_config(self) -> bool:
        """验证配置"""
        return self.package_price > 0


class BillingEngine:
    """计费引擎主类"""
    
    def __init__(self):
        self.strategies: Dict[int, BillingStrategy] = {}
    
    def register_strategy(
        self,
        strategy_id: int,
        billing_type: BillingType,
        config: Dict[str, Any]
    ):
        """注册计费策略"""
        config["strategy_id"] = strategy_id
        
        strategy_map = {
            BillingType.USAGE: UsageBillingStrategy,
            BillingType.TIERED: TieredBillingStrategy,
            BillingType.TIME: TimeBillingStrategy,
            BillingType.PACKAGE: PackageBillingStrategy,
        }
        
        strategy_class = strategy_map.get(billing_type)
        if strategy_class:
            strategy = strategy_class(config)
            if strategy.validate_config():
                self.strategies[strategy_id] = strategy
                return True
        return False
    
    def calculate(
        self,
        strategy_id: int,
        customer_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> Optional[BillingResult]:
        """计算计费"""
        strategy = self.strategies.get(strategy_id)
        if strategy:
            return strategy.calculate(
                customer_id=customer_id,
                period_start=period_start,
                period_end=period_end,
                usage_data=usage_data
            )
        return None
    
    def generate_bill_no(self) -> str:
        """生成账单号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BILL{timestamp}{uuid4().hex[:8].upper()}"


class BillManager:
    """账单管理器"""
    
    def __init__(self, engine: BillingEngine):
        self.engine = engine
    
    def create_bill(
        self,
        customer_id: int,
        strategy_id: int,
        period_start: date,
        period_end: date,
        usage_data: Dict[str, Any]
    ) -> Optional[BillingResult]:
        """创建账单"""
        result = self.engine.calculate(
            strategy_id=strategy_id,
            customer_id=customer_id,
            period_start=period_start,
            period_end=period_end,
            usage_data=usage_data
        )
        return result
    
    def aggregate_bills(
        self,
        customer_id: int,
        bill_results: List[BillingResult]
    ) -> BillingResult:
        """汇总账单"""
        if not bill_results:
            return BillingResult(
                customer_id=customer_id,
                strategy_id=0,
                period_start=date.today(),
                period_end=date.today()
            )
        
        aggregated = BillingResult(
            customer_id=customer_id,
            strategy_id=bill_results[0].strategy_id,
            period_start=bill_results[0].period_start,
            period_end=bill_results[-1].period_end,
            items=[],
            tax_rate=bill_results[0].tax_rate  # 使用第一个账单的税率
        )
        
        # 汇总所有明细
        all_items = []
        for bill in bill_results:
            all_items.extend(bill.items)
        
        # 按项目名称合并
        item_dict: Dict[str, BillingItem] = {}
        for item in all_items:
            if item.item_name not in item_dict:
                item_dict[item.item_name] = BillingItem(
                    item_name=item.item_name,
                    quantity=item.quantity,
                    unit=item.unit,
                    unit_price=item.unit_price,
                    amount=item.amount
                )
            else:
                existing = item_dict[item.item_name]
                existing.quantity += item.quantity
                existing.amount += item.amount
        
        aggregated.items = list(item_dict.values())
        aggregated.calculate_total()
        return aggregated
