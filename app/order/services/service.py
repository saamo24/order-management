
from fastapi import HTTPException, status

from app.models.order import OrderStatus
from app.order.repositories.repository import OrderRepository
from app.customer.repositories.repository import CustomerRepository
from app.order.schemas.order import OrderCreate
from app.product.repositories.repository import ProductRepository
from app.order.serializers.serializer import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, OrderResponse,
    OrderStatusUpdate
)


class OrderService:
    """Order Service."""
    
    def __init__(
        self, 
        repository: OrderRepository,
        serializer: OrderSerializer,
        create_serializer: OrderCreateSerializer,
        update_serializer: OrderUpdateSerializer,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
    ):
        self.repository = repository
        self.serializer = serializer
        self.create_serializer = create_serializer
        self.update_serializer = update_serializer
        self.customer_repository = customer_repository
        self.product_repository = product_repository
    
    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Create a new order with business validation."""
        # Validate that customer exists
        customer = await self.customer_repository.get_by_id(order_data.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Validate that products exist and get their details
        product_ids = [item.product_id for item in order_data.items]
        products = await self.product_repository.get_by_ids(product_ids)
        
        if len(products) != len(product_ids):
            found_ids = {str(p.id) for p in products}
            missing_ids = [pid for pid in product_ids if pid not in found_ids]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Products not found: {missing_ids}"
            )
        
        # Create product lookup dictionary for product details
        product_lookup = {str(p.id): p for p in products}
        
        # Prepare items with product details
        items_with_details = []
        for item in order_data.items:
            product = product_lookup[item.product_id]
            items_with_details.append({
                "product_id": item.product_id,
                "product_name": product.name,
                "quantity": item.quantity,
                "unit_price": product.price
            })
        
        order = await self.repository.create(
            order_data, 
            customer.name, 
            customer.email, 
            items_with_details
        )
        
        return await self.serializer.serialize(order)
    
    async def get_order_by_id(self, order_id: str) -> OrderResponse:
        """Get order by ID."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return await self.serializer.serialize(order)
    
    async def get_all_orders(self, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
        """Get all orders with pagination."""
        orders = await self.repository.get_all(skip, limit)
        return await self.serializer.serialize_for_list(orders)
    
    async def get_orders_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
        """Get orders by customer ID."""
        # Validate that customer exists
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        orders = await self.repository.get_by_customer_id(customer_id, skip, limit)
        return await self.serializer.serialize_for_list(orders)
    
    async def get_orders_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
        """Get orders by status."""
        orders = await self.repository.get_by_status(status, skip, limit)
        return await self.serializer.serialize_for_list(orders)
    
    async def update_order_status(self, order_id: str, new_status: OrderStatusUpdate) -> OrderResponse:
        """Update order status with business validation."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Check if transition is valid for order status
        if not order.can_transition_to(new_status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {order.status} to {new_status}"
            )
        
        updated_order = await self.repository.update_status(order_id, new_status)
        if not updated_order:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update order status"
            )
        
        return await self.serializer.serialize(updated_order)
    
    async def delete_order(self, order_id: str) -> bool:
        """Delete order."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return await self.repository.delete(order_id)
