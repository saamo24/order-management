from fastapi import APIRouter, Depends, Query

from app.container.dependencies import get_order_service
from app.order.services.service import OrderService
from app.order.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.models.order import OrderStatus


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    """Create a new order."""
    return await order_service.create_order(order_data)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(get_order_service)
):
    """Get order by ID."""
    return await order_service.get_order_by_id(order_id)


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    order_service: OrderService = Depends(get_order_service)
):
    """List all orders with pagination."""
    return await order_service.get_all_orders(skip, limit)


@router.get("/customer/{customer_id}", response_model=list[OrderResponse])
async def list_orders_by_customer(
    customer_id: str,
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    order_service: OrderService = Depends(get_order_service)
):
    """List orders by customer ID."""
    return await order_service.get_orders_by_customer_id(customer_id, skip, limit)


@router.get("/status/{status}", response_model=list[OrderResponse])
async def list_orders_by_status(
    status: OrderStatus,
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    order_service: OrderService = Depends(get_order_service)
):
    """List orders by status."""
    return await order_service.get_orders_by_status(status, skip, limit)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    order_service: OrderService = Depends(get_order_service)
):
    """Update order status."""
    return await order_service.update_order_status(order_id, status_update.status)


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: str,
    order_service: OrderService = Depends(get_order_service)
):
    """Delete order."""
    await order_service.delete_order(order_id)
