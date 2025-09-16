from beanie import Document
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class OrderItem(BaseModel):
    """Order item embedded document."""
    
    product_id: str
    product_name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    
    @property
    def total_price(self) -> float:
        """Calculate total price for this item."""
        return self.quantity * self.unit_price


class Order(Document):
    """Order model."""
    
    customer_id: str
    customer_name: str
    customer_email: str
    items: list[OrderItem] = Field(..., min_length=1)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "orders"
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        """Validate that items list is not empty."""
        if not v or len(v) == 0:
            raise ValueError('Order must have at least one item')
        return v
    
    @property
    def total_price(self) -> float:
        """Calculate total price for the order."""
        return sum(item.total_price for item in self.items)
    
    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """Check if order can transition to new status."""
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
            OrderStatus.PAID: [OrderStatus.CANCELLED],
            OrderStatus.CANCELLED: []
        }
        
        return new_status in valid_transitions.get(self.status, [])
