from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: str
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item."""
    pass


class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema."""
    customer_id: str
    items: list[OrderItemCreate] = Field(..., min_items=1)


class OrderCreate(OrderBase):
    """Schema for creating an order."""
    pass


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: OrderStatus | None = None


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: str
    customer_id: str
    customer_name: str
    customer_email: str
    items: list[OrderItemResponse]
    status: OrderStatus
    total_price: float
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status."""
    status: OrderStatus
    
    @validator('status')
    def validate_status(cls, v):
        """Validate status value."""
        if v not in OrderStatus:
            raise ValueError(f'Invalid status: {v}')
        return v
