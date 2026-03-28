"""
支付网关核心模块
统一支付接口，支持多种支付渠道
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4
import hashlib
import json


class PaymentChannel(Enum):
    """支付渠道"""
    ALIPAY = "alipay"
    WECHAT = "wechat"
    UNIONPAY = "unionpay"


class PaymentStatus(Enum):
    """支付状态"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDING = "refunding"
    REFUNDED = "refunded"


@dataclass
class PaymentOrder:
    """支付订单"""
    order_no: str = field(default_factory=lambda: str(uuid4()))
    bill_id: Optional[str] = None
    customer_id: int = 0
    amount: Decimal = Decimal("0.00")
    currency: str = "CNY"
    channel: PaymentChannel = PaymentChannel.ALIPAY
    status: PaymentStatus = PaymentStatus.PENDING
    payment_url: Optional[str] = None
    transaction_id: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    subject: str = ""
    body: str = ""
    notify_url: str = ""
    return_url: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None


@dataclass
class PaymentCallback:
    """支付回调"""
    order_no: str
    channel: PaymentChannel
    callback_data: Dict[str, Any]
    signature: Optional[str] = None
    verified: bool = False
    processed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PaymentResult:
    """支付结果"""
    success: bool
    order_no: str
    status: PaymentStatus
    transaction_id: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


class PaymentAdapter(ABC):
    """支付渠道适配器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.app_id = config.get("app_id", "")
        self.app_secret = config.get("app_secret", "")
        self.notify_url = config.get("notify_url", "")
        self.return_url = config.get("return_url", "")
    
    @abstractmethod
    def create_payment(
        self,
        order: PaymentOrder
    ) -> PaymentResult:
        """创建支付"""
        pass
    
    @abstractmethod
    def query_payment(
        self,
        order_no: str
    ) -> PaymentResult:
        """查询支付状态"""
        pass
    
    @abstractmethod
    def verify_callback(
        self,
        callback_data: Dict[str, Any],
        signature: str
    ) -> bool:
        """验证回调签名"""
        pass
    
    @abstractmethod
    def parse_callback(
        self,
        callback_data: Dict[str, Any]
    ) -> PaymentCallback:
        """解析回调数据"""
        pass
    
    def generate_order_no(self) -> str:
        """生成订单号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PAY{timestamp}{uuid4().hex[:8].upper()}"


class AlipayAdapter(PaymentAdapter):
    """支付宝适配器"""
    
    def create_payment(
        self,
        order: PaymentOrder
    ) -> PaymentResult:
        """创建支付宝支付"""
        try:
            # 模拟支付宝支付创建
            # 实际应用中需要调用支付宝API
            payment_data = {
                "out_trade_no": order.order_no,
                "total_amount": str(order.amount),
                "subject": order.subject,
                "body": order.body,
                "notify_url": order.notify_url or self.notify_url,
                "return_url": order.return_url or self.return_url,
                "product_code": "FAST_INSTANT_TRADE_PAY"
            }
            
            # 生成签名
            signature = self._sign(payment_data)
            payment_data["sign"] = signature
            
            # 构建支付URL（模拟）
            payment_url = f"https://openapi.alipay.com/gateway.do?{self._build_query(payment_data)}"
            
            return PaymentResult(
                success=True,
                order_no=order.order_no,
                status=PaymentStatus.PENDING,
                raw_data={"payment_url": payment_url}
            )
        except Exception as e:
            return PaymentResult(
                success=False,
                order_no=order.order_no,
                status=PaymentStatus.FAILED,
                error_code="CREATE_ERROR",
                error_message=str(e)
            )
    
    def query_payment(
        self,
        order_no: str
    ) -> PaymentResult:
        """查询支付宝支付状态"""
        # 模拟查询
        return PaymentResult(
            success=True,
            order_no=order_no,
            status=PaymentStatus.PENDING,
            raw_data={"query_result": "success"}
        )
    
    def verify_callback(
        self,
        callback_data: Dict[str, Any],
        signature: str
) -> bool:
        """验证支付宝回调签名"""
        # 模拟签名验证
        return signature == self._sign(callback_data)
    
    def parse_callback(
        self,
        callback_data: Dict[str, Any]
    ) -> PaymentCallback:
        """解析支付宝回调数据"""
        return PaymentCallback(
            order_no=callback_data.get("out_trade_no", ""),
            channel=PaymentChannel.ALIPAY,
            callback_data=callback_data,
            signature=callback_data.get("sign", "")
        )
    
    def _sign(self, data: Dict[str, Any]) -> str:
        """生成签名（模拟）"""
        # 实际应用中需要按照支付宝签名规则实现
        sorted_data = sorted(data.items())
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_data if k != "sign"])
        sign_str += f"&key={self.app_secret}"
        return hashlib.md5(sign_str.encode()).hexdigest()
    
    def _build_query(self, data: Dict[str, Any]) -> str:
        """构建查询字符串"""
        return "&".join([f"{k}={v}" for k, v in data.items()])


class WeChatPayAdapter(PaymentAdapter):
    """微信支付适配器"""
    
    def create_payment(
        self,
        order: PaymentOrder
    ) -> PaymentResult:
        """创建微信支付"""
        try:
            # 模拟微信支付创建
            # 实际应用中需要调用微信支付API
            payment_data = {
                "out_trade_no": order.order_no,
                "total_fee": int(order.amount * 100),  # 微信支付金额单位为分
                "body": order.subject,
                "notify_url": order.notify_url or self.notify_url,
                "trade_type": "MWEB"  # H5支付
            }
            
            # 生成签名
            signature = self._sign(payment_data)
            payment_data["sign"] = signature
            
            # 构建支付URL（模拟）
            payment_url = f"https://api.mch.weixin.qq.com/pay/unifiedorder?code_url=weixin://wxpay/bizpayurl?pr={uuid4().hex}"
            
            return PaymentResult(
                success=True,
                order_no=order.order_no,
                status=PaymentStatus.PENDING,
                raw_data={"payment_url": payment_url}
            )
        except Exception as e:
            return PaymentResult(
                success=False,
                order_no=order.order_no,
                status=PaymentStatus.FAILED,
                error_code="CREATE_ERROR",
                error_message=str(e)
            )
    
    def query_payment(
        self,
        order_no: str
    ) -> PaymentResult:
        """查询微信支付状态"""
        # 模拟查询
        return PaymentResult(
            success=True,
            order_no=order_no,
            status=PaymentStatus.PENDING,
            raw_data={"query_result": "success"}
        )
    
    def verify_callback(
        self,
        callback_data: Dict[str, Any],
        signature: str
    ) -> bool:
        """验证微信支付回调签名"""
        # 模拟签名验证
        return signature == self._sign(callback_data)
    
    def parse_callback(
        self,
        callback_data: Dict[str, Any]
    ) -> PaymentCallback:
        """解析微信支付回调数据"""
        return PaymentCallback(
            order_no=callback_data.get("out_trade_no", ""),
            channel=PaymentChannel.WECHAT,
            callback_data=callback_data,
            signature=callback_data.get("sign", "")
        )
    
    def _sign(self, data: Dict[str, Any]) -> str:
        """生成签名（模拟）"""
        # 实际应用中需要按照微信支付签名规则实现
        sorted_data = sorted(data.items())
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_data if k != "sign"])
        sign_str += f"&key={self.app_secret}"
        return hashlib.md5(sign_str.encode()).hexdigest()


class UnionPayAdapter(PaymentAdapter):
    """银联适配器"""
    
    def create_payment(
        self,
        order: PaymentOrder
    ) -> PaymentResult:
        """创建银联支付"""
        try:
            # 模拟银联支付创建
            payment_data = {
                "orderId": order.order_no,
                "txnAmt": int(order.amount * 100),  # 银联金额单位为分
                "txnTime": datetime.now().strftime("%Y%m%d%H%M%S"),
                "currencyCode": "156"  # 人民币
            }
            
            signature = self._sign(payment_data)
            payment_data["signature"] = signature
            
            payment_url = f"https://gateway.95516.com/gateway/api/frontTransReq?data={json.dumps(payment_data)}"
            
            return PaymentResult(
                success=True,
                order_no=order.order_no,
                status=PaymentStatus.PENDING,
                raw_data={"payment_url": payment_url}
            )
        except Exception as e:
            return PaymentResult(
                success=False,
                order_no=order.order_no,
                status=PaymentStatus.FAILED,
                error_code="CREATE_ERROR",
                error_message=str(e)
            )
    
    def query_payment(
        self,
        order_no: str
    ) -> PaymentResult:
        """查询银联支付状态"""
        return PaymentResult(
            success=True,
            order_no=order_no,
            status=PaymentStatus.PENDING,
            raw_data={"query_result": "success"}
        )
    
    def verify_callback(
        self,
        callback_data: Dict[str, Any],
        signature: str
    ) -> bool:
        """验证银联回调签名"""
        return signature == self._sign(callback_data)
    
    def parse_callback(
        self,
        callback_data: Dict[str, Any]
    ) -> PaymentCallback:
        """解析银联回调数据"""
        return PaymentCallback(
            order_no=callback_data.get("orderId", ""),
            channel=PaymentChannel.UNIONPAY,
            callback_data=callback_data,
            signature=callback_data.get("signature", "")
        )
    
    def _sign(self, data: Dict[str, Any]) -> str:
        """生成签名（模拟）"""
        sign_str = json.dumps(data, sort_keys=True)
        sign_str += self.app_secret
        return hashlib.sha256(sign_str.encode()).hexdigest()


class PaymentGateway:
    """支付网关主类"""
    
    def __init__(self):
        self.adapters: Dict[PaymentChannel, PaymentAdapter] = {}
        self.orders: Dict[str, PaymentOrder] = {}
    
    def register_adapter(
        self,
        channel: PaymentChannel,
        adapter: PaymentAdapter
    ):
        """注册支付渠道适配器"""
        self.adapters[channel] = adapter
    
    def create_payment(
        self,
        customer_id: int,
        amount: Decimal,
        channel: PaymentChannel,
        subject: str = "",
        body: str = "",
        notify_url: str = "",
        return_url: str = "",
        bill_id: Optional[str] = None
    ) -> Optional[PaymentOrder]:
        """创建支付订单"""
        adapter = self.adapters.get(channel)
        if not adapter:
            return None
        
        order = PaymentOrder(
            order_no=adapter.generate_order_no(),
            customer_id=customer_id,
            amount=amount,
            channel=channel,
            subject=subject,
            body=body,
            notify_url=notify_url,
            return_url=return_url,
            bill_id=bill_id
        )
        
        result = adapter.create_payment(order)
        
        if result.success:
            order.payment_url = result.raw_data.get("payment_url")
            self.orders[order.order_no] = order
            return order
        
        return None
    
    def query_payment(
        self,
        order_no: str
    ) -> Optional[PaymentResult]:
        """查询支付状态"""
        order = self.orders.get(order_no)
        if not order:
            return None
        
        adapter = self.adapters.get(order.channel)
        if not adapter:
            return None
        
        return adapter.query_payment(order_no)
    
    def handle_callback(
        self,
        channel: PaymentChannel,
        callback_data: Dict[str, Any],
        signature: Optional[str] = None
    ) -> Optional[PaymentCallback]:
        """处理支付回调"""
        adapter = self.adapters.get(channel)
        if not adapter:
            return None
        
        # 解析回调
        callback = adapter.parse_callback(callback_data)
        
        # 验证签名
        if signature:
            callback.verified = adapter.verify_callback(callback_data, signature)
        
        # 查找订单
        order = self.orders.get(callback.order_no)
        if order:
            # 更新订单状态
            if callback.verified and callback.callback_data.get("trade_status") == "TRADE_SUCCESS":
                order.status = PaymentStatus.SUCCESS
                order.transaction_id = callback.callback_data.get("transaction_id")
                order.paid_at = datetime.now()
                order.raw_data = callback.callback_data
                callback.processed = True
        
        return callback
    
    def cancel_payment(
        self,
        order_no: str
    ) -> bool:
        """取消支付"""
        order = self.orders.get(order_no)
        if order and order.status == PaymentStatus.PENDING:
            order.status = PaymentStatus.CANCELLED
            order.updated_at = datetime.now()
            return True
        return False
    
    def get_order(
        self,
        order_no: str
    ) -> Optional[PaymentOrder]:
        """获取支付订单"""
        return self.orders.get(order_no)
