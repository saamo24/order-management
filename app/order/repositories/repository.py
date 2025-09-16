from datetime import datetime
from beanie import PydanticObjectId

from app.models.order import Order, OrderStatus
from app.order.schemas.order import OrderCreate


class OrderRepository:
    """Order Repository."""
    
    async def create(self, order_data: OrderCreate, customer_name: str, customer_email: str, items_with_details: list[dict]) -> Order:
        """Create a new order."""
        order_items = []
        for item_data in items_with_details:
            order_items.append({
                "product_id": item_data["product_id"],
                "product_name": item_data["product_name"],
                "quantity": item_data["quantity"],
                "unit_price": item_data["unit_price"]
            })
        
        order = Order(
            customer_id=order_data.customer_id,
            customer_name=customer_name,
            customer_email=customer_email,
            items=order_items
        )
        return await order.insert()
    
    async def get_by_id(self, order_id: str) -> Order | None:
        """Get order by ID."""
        try:
            return await Order.get(PydanticObjectId(order_id))
        except Exception:
            return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get all orders with pagination."""
        return await Order.find_all().skip(skip).limit(limit).to_list()
    
    async def get_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get orders by customer ID."""
        return await Order.find(Order.customer_id == customer_id).skip(skip).limit(limit).to_list()
    
    async def get_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get orders by status."""
        return await Order.find(Order.status == status).skip(skip).limit(limit).to_list()
    
    async def update_status(self, order_id: str, new_status: OrderStatus) -> Order | None:
        """Update order status."""
        order = await self.get_by_id(order_id)
        if not order:
            return None
        
        if not order.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {order.status} to {new_status}")
        
        order.status = new_status
        order.updated_at = datetime.utcnow()
        return await order.save()
    
    async def delete(self, order_id: str) -> bool:
        """Delete order."""
        order = await self.get_by_id(order_id)
        if not order:
            return False
        
        await order.delete()
        return True
