from app.core.serializers.base import BaseSerializer
from app.models.order import Order, OrderItem
from app.order.schemas.order import (
    OrderCreate, OrderUpdate, OrderResponse, 
    OrderItemResponse, OrderStatusUpdate
)


class OrderItemSerializer(BaseSerializer[OrderItem, OrderItemResponse]):
    """Serializer for OrderItem domain model."""
    
    async def serialize(self, item: OrderItem) -> OrderItemResponse:
        """Serialize OrderItem to OrderItemResponse."""
        return OrderItemResponse(
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price
        )


class OrderSerializer(BaseSerializer[Order, OrderResponse]):
    """Serializer for Order domain model."""
    
    def __init__(self):
        self.item_serializer = OrderItemSerializer()
    
    async def serialize(self, order: Order) -> OrderResponse:
        """Serialize Order to OrderResponse."""
        # Serialize order items
        items = [await self.item_serializer.serialize(item) for item in order.items]
        
        return OrderResponse(
            id=str(order.id),
            customer_id=order.customer_id,
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            items=items,
            status=order.status,
            total_price=order.total_price,
            created_at=order.created_at,
            updated_at=order.updated_at
        )

    
    async def serialize_for_list(self, orders: list[Order]) -> list[OrderResponse]:
        """Serialize list of orders."""
        return [await self.serialize(order) for order in orders]


class OrderCreateSerializer(BaseSerializer[OrderCreate, OrderResponse]):
    """Serializer for OrderCreate operations."""
    
    async def serialize(self, data: OrderCreate) -> OrderResponse:
        """Serialize OrderCreate to dictionary."""
        return OrderResponse(
            id=str(data.id),
            customer_id=data.customer_id,
            customer_name=data.customer_name,
            customer_email=data.customer_email,
            items=data.items,
            status=data.status,
            total_price=data.total_price,
            created_at=data.created_at,
            updated_at=data.updated_at
        )
    


class OrderUpdateSerializer(BaseSerializer[OrderUpdate, OrderResponse]):
    """Serializer for OrderUpdate operations."""
    
    async def serialize(self, data: OrderUpdate) -> OrderResponse:
        """Serialize OrderUpdate to dictionary."""
        return OrderResponse(
            id=str(data.id),
            customer_id=data.customer_id,
            customer_name=data.customer_name,
            customer_email=data.customer_email,
            items=data.items,
            status=data.status,
            total_price=data.total_price,
            created_at=data.created_at,
            updated_at=data.updated_at
        )


class OrderStatusUpdateSerializer(BaseSerializer[OrderStatusUpdate, OrderStatusUpdate]):
    """Serializer for OrderStatusUpdate operations."""
    
    async def serialize(self, data: OrderStatusUpdate) -> OrderStatusUpdate:
        """Serialize OrderStatusUpdate to dictionary."""
        return OrderStatusUpdate(
            id=data.id,
            status=data.status
        )
