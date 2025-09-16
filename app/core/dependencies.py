from functools import lru_cache

from app.customer.repositories.repository import CustomerRepository
from app.product.repositories.repository import ProductRepository
from app.order.repositories.repository import OrderRepository
from app.customer.services.service import CustomerService
from app.product.services.service import ProductService
from app.order.services.service import OrderService


@lru_cache()
def get_customer_repository() -> CustomerRepository:
    """Get customer repository instance."""
    return CustomerRepository()


@lru_cache()
def get_product_repository() -> ProductRepository:
    """Get product repository instance."""
    return ProductRepository()


@lru_cache()
def get_order_repository() -> OrderRepository:
    """Get order repository instance."""
    return OrderRepository()


@lru_cache()
def get_customer_service() -> CustomerService:
    """Get customer service instance."""
    return CustomerService(get_customer_repository())


@lru_cache()
def get_product_service() -> ProductService:
    """Get product service instance."""
    return ProductService(get_product_repository())


@lru_cache()
def get_order_service() -> OrderService:
    """Get order service instance."""
    return OrderService(
        get_order_repository(),
        get_customer_repository(),
        get_product_repository()
    )
