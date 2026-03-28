"""
支付网关单元测试
"""

import pytest
from decimal import Decimal

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from payment_gateway.gateway import (
    PaymentGateway,
    PaymentChannel,
    PaymentStatus,
    PaymentOrder,
    PaymentResult,
    AlipayAdapter,
    WeChatPayAdapter,
    UnionPayAdapter
)


class TestPaymentAdapters:
    """测试支付渠道适配器"""
    
    def test_alipay_adapter_create_payment(self):
        """测试支付宝适配器创建支付"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = AlipayAdapter(config)
        
        order = PaymentOrder(
            order_no="TEST001",
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单",
            body="测试商品"
        )
        
        result = adapter.create_payment(order)
        
        assert result.success is True
        assert result.order_no == "TEST001"
    
    def test_wechat_adapter_create_payment(self):
        """测试微信支付适配器创建支付"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = WeChatPayAdapter(config)
        
        order = PaymentOrder(
            order_no="TEST002",
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.WECHAT,
            subject="测试订单"
        )
        
        result = adapter.create_payment(order)
        
        assert result.success is True
        assert result.order_no == "TEST002"
    
    def test_unionpay_adapter_create_payment(self):
        """测试银联适配器创建支付"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = UnionPayAdapter(config)
        
        order = PaymentOrder(
            order_no="TEST003",
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.UNIONPAY,
            subject="测试订单"
        )
        
        result = adapter.create_payment(order)
        
        assert result.success is True
        assert result.order_no == "TEST003"
    
    def test_adapter_generate_order_no(self):
        """测试生成订单号"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = AlipayAdapter(config)
        order_no = adapter.generate_order_no()
        
        assert order_no.startswith("PAY")
        assert len(order_no) > 8
    
    def test_adapter_query_payment(self):
        """测试查询支付状态"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = AlipayAdapter(config)
        result = adapter.query_payment("TEST001")
        
        assert result.success is True
        assert result.order_no == "TEST001"
    
    def test_adapter_verify_callback(self):
        """测试验证回调签名"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = AlipayAdapter(config)
        
        callback_data = {
            "out_trade_no": "TEST001",
            "trade_status": "TRADE_SUCCESS"
        }
        
        # 生成签名
        signature = adapter._sign(callback_data)
        
        # 验证签名
        verified = adapter.verify_callback(callback_data, signature)
        
        assert verified is True
    
    def test_adapter_parse_callback(self):
        """测试解析回调数据"""
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_secret"
        }
        
        adapter = AlipayAdapter(config)
        
        callback_data = {
            "out_trade_no": "TEST001",
            "trade_status": "TRADE_SUCCESS",
            "transaction_id": "TXN001",
            "sign": "test_sign"
        }
        
        callback = adapter.parse_callback(callback_data)
        
        assert callback.order_no == "TEST001"
        assert callback.channel == PaymentChannel.ALIPAY
        assert callback.signature == "test_sign"


class TestPaymentGateway:
    """测试支付网关"""
    
    def setup_method(self):
        """设置测试环境"""
        self.gateway = PaymentGateway()
        
        # 注册支付渠道
        alipay_adapter = AlipayAdapter({
            "app_id": "alipay_app_id",
            "app_secret": "alipay_secret"
        })
        self.gateway.register_adapter(PaymentChannel.ALIPAY, alipay_adapter)
        
        wechat_adapter = WeChatPayAdapter({
            "app_id": "wechat_app_id",
            "app_secret": "wechat_secret"
        })
        self.gateway.register_adapter(PaymentChannel.WECHAT, wechat_adapter)
    
    def test_register_adapter(self):
        """测试注册支付渠道适配器"""
        unionpay_adapter = UnionPayAdapter({
            "app_id": "unionpay_app_id",
            "app_secret": "unionpay_secret"
        })
        
        self.gateway.register_adapter(PaymentChannel.UNIONPAY, unionpay_adapter)
        
        assert PaymentChannel.UNIONPAY in self.gateway.adapters
    
    def test_create_alipay_payment(self):
        """测试创建支付宝支付"""
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单",
            body="测试商品"
        )
        
        assert order is not None
        assert order.customer_id == 1001
        assert order.amount == Decimal("100.00")
        assert order.channel == PaymentChannel.ALIPAY
        assert order.status == PaymentStatus.PENDING
        assert order.payment_url is not None
        assert order.order_no in self.gateway.orders
    
    def test_create_wechat_payment(self):
        """测试创建微信支付"""
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("200.00"),
            channel=PaymentChannel.WECHAT,
            subject="测试订单"
        )
        
        assert order is not None
        assert order.customer_id == 1001
        assert order.amount == Decimal("200.00")
        assert order.channel == PaymentChannel.WECHAT
        assert order.status == PaymentStatus.PENDING
    
    def test_create_payment_with_invalid_channel(self):
        """测试创建不支持的支付渠道"""
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.UNIONPAY,
            subject="测试订单"
        )
        
        assert order is None
    
    def test_query_payment(self):
        """测试查询支付状态"""
        # 先创建订单
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单"
        )
        
        # 查询支付状态
        result = self.gateway.query_payment(order.order_no)
        
        assert result is not None
        assert result.order_no == order.order_no
        assert result.success is True
    
    def test_handle_callback(self):
        """测试处理支付回调"""
        # 先创建订单
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单"
        )
        
        # 模拟回调数据
        callback_data = {
            "out_trade_no": order.order_no,
            "trade_status": "TRADE_SUCCESS",
            "transaction_id": "TXN001"
        }
        
        # 生成签名
        adapter = self.gateway.adapters[PaymentChannel.ALIPAY]
        signature = adapter._sign(callback_data)
        callback_data["sign"] = signature
        
        # 处理回调
        callback = self.gateway.handle_callback(
            channel=PaymentChannel.ALIPAY,
            callback_data=callback_data,
            signature=signature
        )
        
        assert callback is not None
        assert callback.order_no == order.order_no
        assert callback.verified is True
        assert callback.processed is True
        
        # 验证订单状态已更新
        updated_order = self.gateway.get_order(order.order_no)
        assert updated_order.status == PaymentStatus.SUCCESS
        assert updated_order.transaction_id == "TXN001"
    
    def test_cancel_payment(self):
        """测试取消支付"""
        # 创建订单
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单"
        )
        
        # 取消支付
        result = self.gateway.cancel_payment(order.order_no)
        
        assert result is True
        
        # 验证订单状态
        updated_order = self.gateway.get_order(order.order_no)
        assert updated_order.status == PaymentStatus.CANCELLED
    
    def test_cancel_paid_payment(self):
        """测试取消已支付的订单"""
        # 创建订单
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单"
        )
        
        # 模拟支付成功
        order.status = PaymentStatus.SUCCESS
        
        # 尝试取消
        result = self.gateway.cancel_payment(order.order_no)
        
        assert result is False
    
    def test_get_order(self):
        """测试获取订单"""
        # 创建订单
        order = self.gateway.create_payment(
            customer_id=1001,
            amount=Decimal("100.00"),
            channel=PaymentChannel.ALIPAY,
            subject="测试订单"
        )
        
        # 获取订单
        retrieved = self.gateway.get_order(order.order_no)
        
        assert retrieved is not None
        assert retrieved.order_no == order.order_no
        assert retrieved.customer_id == 1001
    
    def test_get_nonexistent_order(self):
        """测试获取不存在的订单"""
        order = self.gateway.get_order("NONEXISTENT")
        
        assert order is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
