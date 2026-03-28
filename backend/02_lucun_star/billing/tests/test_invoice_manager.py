"""
发票管理单元测试
"""

import pytest
from datetime import date, datetime
from decimal import Decimal

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from invoice_manager.manager import (
    InvoiceManager,
    InvoiceType,
    InvoiceStatus,
    InvoiceInfo,
    InvoiceItem,
    MockTaxSystemClient
)


class TestInvoiceManager:
    """测试发票管理器"""
    
    def setup_method(self):
        """设置测试环境"""
        self.manager = InvoiceManager()
    
    def test_create_invoice(self):
        """测试创建发票"""
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
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00"),
            address="北京市朝阳区",
            phone="13800138000",
            bank_name="招商银行",
            bank_account="1234567890123456"
        )
        
        assert invoice is not None
        assert invoice.customer_id == 1001
        assert invoice.bill_id == "BILL001"
        assert invoice.type == InvoiceType.ELECTRONIC
        assert invoice.title == "测试公司"
        assert invoice.tax_no == "91110000MA00000000"
        assert len(invoice.items) == 1
        assert invoice.amount == Decimal("1000.00")
        assert invoice.tax_amount == Decimal("60.00")
        assert invoice.total_amount == Decimal("1060.00")
        assert invoice.status == InvoiceStatus.DRAFT
        assert invoice.invoice_no in self.manager.invoices
    
    def test_create_invoice_with_multiple_items(self):
        """测试创建包含多个明细的发票"""
        items = [
            InvoiceItem(
                item_name="云服务器",
                item_code="CLOUD-001",
                quantity=Decimal("1"),
                unit="台",
                unit_price=Decimal("1000.00"),
                amount=Decimal("1000.00")
            ),
            InvoiceItem(
                item_name="数据存储",
                item_code="STORAGE-001",
                quantity=Decimal("100"),
                unit="GB",
                unit_price=Decimal("1.00"),
                amount=Decimal("100.00")
            )
        ]
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        assert invoice is not None
        assert len(invoice.items) == 2
        assert invoice.amount == Decimal("1100.00")
        assert invoice.tax_amount == Decimal("66.00")
        assert invoice.total_amount == Decimal("1166.00")
    
    def test_issue_invoice(self):
        """测试开具发票"""
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
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 开具发票
        result = self.manager.issue_invoice(invoice.invoice_no)
        
        assert result is True
        assert invoice.status == InvoiceStatus.ISSUED
        assert invoice.issued_at is not None
        assert invoice.pdf_url is not None
    
    def test_issue_nonexistent_invoice(self):
        """测试开具不存在的发票"""
        result = self.manager.issue_invoice("NONEXISTENT")
        assert result is False
    
   
    
    def test_cancel_draft_invoice(self):
        """测试作废草稿发票"""
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
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 作废发票
        result = self.manager.cancel_invoice(invoice.invoice_no)
        
        assert result is True
        assert invoice.status == InvoiceStatus.CANCELLED
    
    def test_cancel_issued_invoice(self):
        """测试作废已开具的发票"""
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
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 先开具发票
        self.manager.issue_invoice(invoice.invoice_no)
        
        # 作废发票
        result = self.manager.cancel_invoice(invoice.invoice_no)
        
        assert result is True
        assert invoice.status == InvoiceStatus.CANCELLED
    
    def test_get_invoice(self):
        """测试获取发票信息"""
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
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 获取发票
        retrieved = self.manager.get_invoice(invoice.invoice_no)
        
        assert retrieved is not None
        assert retrieved.invoice_no == invoice.invoice_no
        assert retrieved.customer_id == 1001
        assert retrieved.title == "测试公司"
    
    def test_query_invoice_status(self):
        """测试查询发票状态"""
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
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 开具发票
        self.manager.issue_invoice(invoice.invoice_no)
        
        # 查询状态
        status = self.manager.query_invoice_status(invoice.invoice_no)
        
        assert status == "success"
    
    def test_generate_invoice_html(self):
        """测试生成发票HTML"""
        items = [
            InvoiceItem(
                item_name="云服务器",
                item_code="CLOUD-001",
                quantity=Decimal("1"),
                unit="台",
                unit_price=Decimal("1000.00"),
                amount=Decimal("1000.00"),
                tax_rate=Decimal("6.00"),
                tax_amount=Decimal("60.00")
            )
        ]
        
        invoice = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00"),
            address="北京市朝阳区",
            phone="13800138000",
            bank_name="招商银行",
            bank_account="1234567890123456"
        )
        
        # 生成HTML
        html = self.manager.generate_invoice_html(invoice.invoice_no)
        
        assert html is not None
        assert "<!DOCTYPE html>" in html
        assert "测试公司" in html
        assert "91110000MA00000000" in html
        assert "云服务器" in html
        assert "1000.00" in html
    
    def test_list_invoices_by_customer(self):
        """测试按客户查询发票列表"""
        # 创建多个发票
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
        
        invoice1 = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司1",
            tax_no="91110000MA00000001",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        invoice2 = self.manager.create_invoice(
            customer_id=1002,
            bill_id="BILL002",
            type=InvoiceType.ELECTRONIC,
            title="测试公司2",
            tax_no="91110000MA00000002",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        invoice3 = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL003",
            type=InvoiceType.ELECTRONIC,
            title="测试公司1",
            tax_no="91110000MA00000001",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 查询客户1001的发票
        invoices = self.manager.list_invoices(customer_id=1001)
        
        assert len(invoices) == 2
        assert all(invoice.customer_id == 1001 for invoice in invoices)
    
    def test_list_invoices_by_status(self):
        """测试按状态查询发票列表"""
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
        
        # 创建并开具发票
        invoice1 = self.manager.create_invoice(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        self.manager.issue_invoice(invoice1.invoice_no)
        
        # 创建草稿发票
        invoice2 = self.manager.create_invoice(
            customer_id=1002,
            bill_id="BILL002",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000",
            items=items,
            tax_rate=Decimal("6.00")
        )
        
        # 查询已开具的发票
        issued_invoices = self.manager.list_invoices(status=InvoiceStatus.ISSUED)
        
        assert len(issued_invoices) == 1
        assert issued_invoices[0].status == InvoiceStatus.ISSUED
        
        # 查询草稿发票
        draft_invoices = self.manager.list_invoices(status=InvoiceStatus.DRAFT)
        
        assert len(draft_invoices) == 1
        assert draft_invoices[0].status == InvoiceStatus.DRAFT
    
    def test_generate_invoice_from_bill(self):
        """测试从账单生成发票"""
        bill_items = [
            {
                "item_name": "云服务器",
                "item_code": "CLOUD-001",
                "quantity": "1",
                "unit": "台",
                "unit_price": "1000.00",
                "amount": "1000.00"
            },
            {
                "item_name": "数据存储",
                "item_code": "STORAGE-001",
                "quantity": "100",
                "unit": "GB",
                "unit_price": "1.00",
                "amount": "100.00"
            }
        ]
        
        invoice = self.manager.generate_invoice_from_bill(
            bill_id="BILL001",
            customer_id=1001,
            title="测试公司",
            tax_no="91110000MA00000000",
            bill_items=bill_items,
            tax_rate=Decimal("6.00")
        )
        
        assert invoice is not None
        assert len(invoice.items) == 2
        assert invoice.amount == Decimal("1100.00")
        assert invoice.total_amount == Decimal("1166.00")


class TestMockTaxSystemClient:
    """测试模拟税控系统客户端"""
    
    def setup_method(self):
        """设置测试环境"""
        self.client = MockTaxSystemClient()
    
    def test_apply_invoice(self):
        """测试申请开具发票"""
        invoice = InvoiceInfo(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000"
        )
        
        result = self.client.apply_invoice(invoice)
        
        assert result is True
        assert invoice.invoice_no in self.client.invoices
    
    def test_query_invoice(self):
        """测试查询发票"""
        invoice = InvoiceInfo(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000"
        )
        
        self.client.apply_invoice(invoice)
        
        result = self.client.query_invoice(invoice.invoice_no)
        
        assert result is not None
        assert result["invoice_no"] == invoice.invoice_no
        assert "pdf_url" in result
    
    def test_cancel_invoice(self):
        """测试作废发票"""
        invoice = InvoiceInfo(
            customer_id=1001,
            bill_id="BILL001",
            type=InvoiceType.ELECTRONIC,
            title="测试公司",
            tax_no="91110000MA00000000"
        )
        
        self.client.apply_invoice(invoice)
        
        result = self.client.cancel_invoice(invoice.invoice_no)
        
        assert result is True
        assert self.client.invoices[invoice.invoice_no]["status"] == "cancelled"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
