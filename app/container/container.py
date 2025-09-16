from dependency_injector import containers, providers

from app.container.config import Config
from app.customer.repositories.repository import CustomerRepository
from app.product.repositories.repository import ProductRepository
from app.order.repositories.repository import OrderRepository
from app.customer.services.service import CustomerService
from app.product.services.service import ProductService
from app.order.services.service import OrderService
from app.customer.serializers.serializer import (
    CustomerSerializer, CustomerCreateSerializer, CustomerUpdateSerializer
)
from app.product.serializers.serializer import (
    ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer
)
from app.order.serializers.serializer import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, OrderStatusUpdateSerializer
)


class Container(containers.DeclarativeContainer):
    """Main dependency injection container using dependency-injector."""
    
    # Configuration
    config = Config()
    
    # Repositories
    customer_repository = providers.Factory(CustomerRepository)
    product_repository = providers.Factory(ProductRepository)
    order_repository = providers.Factory(OrderRepository)
    
    # Serializers
    customer_serializer = providers.Factory(CustomerSerializer)
    customer_create_serializer = providers.Factory(CustomerCreateSerializer)
    customer_update_serializer = providers.Factory(CustomerUpdateSerializer)
    
    product_serializer = providers.Factory(ProductSerializer)
    product_create_serializer = providers.Factory(ProductCreateSerializer)
    product_update_serializer = providers.Factory(ProductUpdateSerializer)
    
    order_serializer = providers.Factory(OrderSerializer)
    order_create_serializer = providers.Factory(OrderCreateSerializer)
    order_update_serializer = providers.Factory(OrderUpdateSerializer)
    order_status_update_serializer = providers.Factory(OrderStatusUpdateSerializer)
    
    # Services
    customer_service = providers.Factory(
        CustomerService,
        customer_repository=customer_repository,
        customer_serializer=customer_serializer,
        customer_create_serializer=customer_create_serializer,
        customer_update_serializer=customer_update_serializer,
    )
    
    product_service = providers.Factory(
        ProductService,
        product_repository=product_repository,
        product_serializer=product_serializer,
        product_create_serializer=product_create_serializer,
        product_update_serializer=product_update_serializer,
    )
    
    order_service = providers.Factory(
        OrderService,
        order_repository=order_repository,
        customer_repository=customer_repository,
        product_repository=product_repository,
        order_serializer=order_serializer,
        order_create_serializer=order_create_serializer,
        order_update_serializer=order_update_serializer,
    )


# Global container instance
container = Container()
