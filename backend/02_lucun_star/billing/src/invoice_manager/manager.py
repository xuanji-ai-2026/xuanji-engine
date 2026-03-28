"""
发票管理核心模块
负责发票生成、开具、管理
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
import json


class InvoiceType(Enum):
    """发票类型"""
    NORMAL = "normal"  # 普通发票
    VAT_SPECIAL = "vat_special"  # 增值税专用发票
    ELECTRONIC = "electronic"  # 电子发票
    PAPER = "paper"  # 纸质发票


class InvoiceStatus(Enum):
    """发票状态"""
    DRAFT = "draft"
    ISSUED = "issued"
    INVALID = "invalid"
    CANCELLED = "cancelled"


@dataclass
class InvoiceItem:
    """发票明细项"""
    item_id: str = field(default_factory=lambda: str(uuid4()))
    item_name: str = ""
    item_code: str = ""
    quantity: Decimal = Decimal("0")
    unit: str = ""
    unit_price: Decimal = Decimal("0.00")
    amount: Decimal = Decimal("0.00")
    tax_rate: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")


@dataclass
class InvoiceInfo:
    """发票信息"""
    invoice_no: str = field(default_factory=lambda: f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid4().hex[:8].upper()}")
    bill_id: Optional[str] = None
    customer_id: int = 0
    type: InvoiceType = InvoiceType.NORMAL
    status: InvoiceStatus = InvoiceStatus.DRAFT
    
    # 发票抬头信息
    title: str = ""
    tax_no: str = ""
    address: str = ""
    phone: str = ""
    bank_name: str = ""
    bank_account: str = ""
    
    # 金额信息
    items: List[InvoiceItem] = field(default_factory=list)
    amount: Decimal = Decimal("0.00")  # 不含税金额
    tax_rate: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    total_amount: Decimal = Decimal("0.00")  # 含税金额
    
    # 其他信息
    remarks: str = ""
    pdf_url: Optional[str] = None
    
    # 时间信息
    created_at: datetime = field(default_factory=datetime.now)
    issued_at: Optional[datetime] = None
    
    def calculate_total(self):
        """计算总金额"""
        self.amount = sum(item.amount for item in self.items)
        self.tax_amount = self.amount * self.tax_rate / Decimal("100")
        self.total_amount = self.amount + self.tax_amount


class TaxSystemClient(ABC):
    """税控系统客户端基类"""
    
    @abstractmethod
    def apply_invoice(self, invoice: InvoiceInfo) -> bool:
        """申请开具发票"""
        pass
    
    @abstractmethod
    def query_invoice(self, invoice_no: str) -> Optional[Dict[str, Any]]:
        """查询发票状态"""
        pass
    
    @abstractmethod
    def cancel_invoice(self, invoice_no: str) -> bool:
        """作废发票"""
        pass


class MockTaxSystemClient(TaxSystemClient):
    """模拟税控系统客户端"""
    
    def __init__(self):
        self.invoices: Dict[str, Dict[str, Any]] = {}
    
    def apply_invoice(self, invoice: InvoiceInfo) -> bool:
        """申请开具发票（模拟）"""
        invoice_data = {
            "invoice_no": invoice.invoice_no,
            "status": "success",
            "pdf_url": f"https://example.com/invoices/{invoice.invoice_no}.pdf"
        }
        self.invoices[invoice.invoice_no] = invoice_data
        return True
    
    def query_invoice(self, invoice_no: str) -> Optional[Dict[str, Any]]:
        """查询发票状态（模拟）"""
        return self.invoices.get(invoice_no)
    
    def cancel_invoice(self, invoice_no: str) -> bool:
        """作废发票（模拟）"""
        if invoice_no in self.invoices:
            self.invoices[invoice_no]["status"] = "cancelled"
            return True
        return False


class InvoiceTemplate:
    """发票模板管理"""
    
    @staticmethod
    def render_invoice_html(invoice: InvoiceInfo) -> str:
        """渲染发票HTML"""
        items_html = ""
        for item in invoice.items:
            items_html += f"""
            <tr>
                <td>{item.item_name}</td>
                <td>{item.item_code}</td>
                <td>{item.quantity}</td>
                <td>{item.unit}</td>
                <td>{item.unit_price}</td>
                <td>{item.amount}</td>
                <td>{item.tax_rate}%</td>
                <td>{item.tax_amount}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>发票 - {invoice.invoice_no}</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .info-table th, .info-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                .item-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .item-table th, .item-table td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                .total {{ text-align: right; font-size: 18px; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>发票</h1>
                <h2>发票号码: {invoice.invoice_no}</h2>
            </div>
            
            <table class="info-table">
                <tr>
                    <th>发票类型</th>
                    <td>{invoice.type.value}</td>
                    <th>开票日期</th>
                    <td>{invoice.issued_at.strftime('%Y-%m-%d') if invoice.issued_at else ''}</td>
                </tr>
                <tr>
                    <th>购买方名称</th>
                    <td>{invoice.title}</td>
                    <th>纳税人识别号</th>
                    <td>{invoice.tax_no}</td>
                </tr>
                <tr>
                    <th>地址电话</th>
                    <td>{invoice.address} {invoice.phone}</td>
                    <th>开户行及账号</th>
                    <td>{invoice.bank_name} {invoice.bank_account}</td>
                </tr>
            </table>
            
            <table class="item-table">
                <thead>
                    <tr>
                        <th>货物或应税劳务名称</th>
                        <th>规格型号</th>
                        <th>数量</th>
                        <th>单位</th>
                        <th>单价</th>
                        <th>金额</th>
                        <th>税率</th>
                        <th>税额</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div class="total">
                <p>价税合计（大写）: {InvoiceTemplate._convert_to_chinese_amount(invoice.total_amount)}</p>
                <p>价税合计（小写）: ￥{invoice.total_amount}</p>
            </div>
            
            <div class="footer">
                <p>备注: {invoice.remarks}</p>
                <p>本发票为电子发票，具有同等法律效力</p>
            </div>
        </body>
        </html>
        """
        return html
    
    @staticmethod
    def _convert_to_chinese_amount(amount: Decimal) -> str:
        """将金额转换为中文大写"""
        # 简化实现，实际需要完整实现
        chinese_nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        chinese_units = ['分', '角', '元', '拾', '佰', '仟', '万']
        
        amount_int = int(amount * 100)
        if amount_int == 0:
            return "零元整"
        
        result = ""
        for i, unit in enumerate(chinese_units):
            digit = amount_int % 10
            if digit != 0:
                result = chinese_nums[digit] + unit + result
            amount_int //= 10
        
        return result + "整"


class InvoiceManager:
    """发票管理器"""
    
    def __init__(self, tax_system_client: Optional[TaxSystemClient] = None):
        self.tax_system_client = tax_system_client or MockTaxSystemClient()
        self.invoices: Dict[str, InvoiceInfo] = {}
        self.templates = InvoiceTemplate()
    
    def create_invoice(
        self,
        customer_id: int,
        bill_id: str,
        type: InvoiceType,
        title: str,
        tax_no: str,
        items: List[InvoiceItem],
        tax_rate: Decimal = Decimal("6.00"),
        **kwargs
    ) -> Optional[InvoiceInfo]:
        """创建发票"""
        invoice = InvoiceInfo(
            customer_id=customer_id,
            bill_id=bill_id,
            type=type,
            title=title,
            tax_no=tax_no,
            items=items,
            tax_rate=tax_rate,
            **kwargs
        )
        
        invoice.calculate_total()
        self.invoices[invoice.invoice_no] = invoice
        return invoice
    
    def issue_invoice(self, invoice_no: str) -> bool:
        """开具发票"""
        invoice = self.invoices.get(invoice_no)
        if not invoice:
            return False
        
        if invoice.status != InvoiceStatus.DRAFT:
            return False
        
        # 调用税控系统申请开具
        success = self.tax_system_client.apply_invoice(invoice)
        
        if success:
            invoice.status = InvoiceStatus.ISSUED
            invoice.issued_at = datetime.now()
            
            # 获取发票PDF
            result = self.tax_system_client.query_invoice(invoice_no)
            if result:
                invoice.pdf_url = result.get("pdf_url")
        
        return success
    
    def cancel_invoice(self, invoice_no: str) -> bool:
        """作废发票"""
        invoice = self.invoices.get(invoice_no)
        if not invoice:
            return False
        
        if invoice.status not in [InvoiceStatus.DRAFT, InvoiceStatus.ISSUED]:
            return False
        
        # 对于已开具的发票，需要调用税控系统作废
        if invoice.status == InvoiceStatus.ISSUED:
            success = self.tax_system_client.cancel_invoice(invoice_no)
            if success:
                invoice.status = InvoiceStatus.CANCELLED
            return success
        else:
            # 对于草稿状态的发票，直接标记为已作废
            invoice.status = InvoiceStatus.CANCELLED
            return True
    
    def get_invoice(self, invoice_no: str) -> Optional[InvoiceInfo]:
        """获取发票信息"""
        return self.invoices.get(invoice_no)
    
    def query_invoice_status(self, invoice_no: str) -> Optional[str]:
        """查询发票状态"""
        result = self.tax_system_client.query_invoice(invoice_no)
        if result:
            return result.get("status")
        return None
    
    def generate_invoice_html(self, invoice_no: str) -> Optional[str]:
        """生成发票HTML"""
        invoice = self.invoices.get(invoice_no)
        if not invoice:
            return None
        
        return self.templates.render_invoice_html(invoice)
    
    def list_invoices(
        self,
        customer_id: Optional[int] = None,
        status: Optional[InvoiceStatus] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> List[InvoiceInfo]:
        """查询发票列表"""
        result = []
        
        for invoice in self.invoices.values():
            # 过滤条件
            if customer_id and invoice.customer_id != customer_id:
                continue
            
            if status and invoice.status != status:
                continue
            
            if start_date and invoice.created_at.date() < start_date:
                continue
            
           
            
            if end_date and invoice.created_at.date() > end_date:
                continue
            
            result.append(invoice)
            
            if len(result) >= limit:
                break
        
        # 按创建时间倒序
        result.sort(key=lambda x: x.created_at, reverse=True)
        return result
    
    def generate_invoice_from_bill(
        self,
        bill_id: str,
        customer_id: int,
        title: str,
        tax_no: str,
        bill_items: List[Any],
        tax_rate: Decimal = Decimal("6.00")
    ) -> Optional[InvoiceInfo]:
        """从账单生成发票"""
       
        
        invoice_items = []
        for idx, item in enumerate(bill_items):
            invoice_items.append(InvoiceItem(
                item_name=item.get("item_name", f"项目{idx + 1}"),
                item_code=item.get("item_code", ""),
                quantity=Decimal(str(item.get("quantity", "0"))),
                unit=item.get("unit", ""),
                unit_price=Decimal(str(item.get("unit_price", "0.00"))),
                amount=Decimal(str(item.get("amount", "0.00")))
            ))
        
        return self.create_invoice(
            customer_id=customer_id,
            bill_id=bill_id,
            type=InvoiceType.ELECTRONIC,
            title=title,
            tax_no=tax_no,
            items=invoice_items,
            tax_rate=tax_rate
        )
