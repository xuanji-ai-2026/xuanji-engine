"""
Market Module
Author: 穆产品 (Employee ID: 169)
Group: XJ-10 辅弼星辰
Task: 市场模块实现
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time


class MarketStatus(Enum):
    """Market status."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Product:
    """Product data class."""
    product_id: str
    name: str
    description: str
    price: float
    category: str
    status: MarketStatus
    created_at: float = field(default_factory=time.time)


class MarketModule:
    """Market Module Implementation"""
    
    def __init__(self):
        """Initialize the market module."""
        self.products: Dict[str, Product] = {}
        self.categories: Dict[str, List[str]] = {}
        
    def create_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str
    ) -> Product:
        """Create a new product."""
        product = Product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            category=category,
            status=MarketStatus.DRAFT
        )
        
        self.products[product_id] = product
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(product_id)
        
        return product
        
    def publish_product(self, product_id: str) -> bool:
        """Publish a product."""
        if product_id in self.products:
            self.products[product_id].status = MarketStatus.PUBLISHED
            return True
        return False
        
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        return self.products.get(product_id)
        
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category."""
        if category not in self.categories:
            return []
        return [self.products[pid] for pid in self.categories[category] if pid in self.products]
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "products_count": len(self.products),
            "categories_count": len(self.categories)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "MarketModule",
            "version": "1.0.0",
            "status": "ready"
        }
