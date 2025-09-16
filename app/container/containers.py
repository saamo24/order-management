"""
Consolidated containers for all domains using dependency-injector.
"""

from dependency_injector import containers, providers

from app.container.config import Config

from app.customer.repositories.repository import CustomerRepository
from app.customer.services.service import CustomerService
from app.customer.serializers.serializer import (
    CustomerSerializer, CustomerCreateSerializer, CustomerUpdateSerializer
)

from app.product.repositories.repository import ProductRepository
from app.product.services.service import ProductService
from app.product.serializers.serializer import (
    ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer
)

from app.order.repositories.repository import OrderRepository
from app.order.services.service import OrderService
from app.order.serializers.serializer import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, OrderStatusUpdateSerializer
)


class CustomerContainer(containers.DeclarativeContainer):
    
    customer_repository = providers.Factory(CustomerRepository)
    
    customer_serializer = providers.Factory(CustomerSerializer)
    customer_create_serializer = providers.Factory(CustomerCreateSerializer)
    customer_update_serializer = providers.Factory(CustomerUpdateSerializer)
    
    customer_service = providers.Factory(
        CustomerService,
        repository=customer_repository,
        serializer=customer_serializer,
        create_serializer=customer_create_serializer,
        update_serializer=customer_update_serializer,
    )


class ProductContainer(containers.DeclarativeContainer):
    
    product_repository = providers.Factory(ProductRepository)
    
    product_serializer = providers.Factory(ProductSerializer)
    product_create_serializer = providers.Factory(ProductCreateSerializer)
    product_update_serializer = providers.Factory(ProductUpdateSerializer)
    
    product_service = providers.Factory(
        ProductService,
        repository=product_repository,
        serializer=product_serializer,
        create_serializer=product_create_serializer,
        update_serializer=product_update_serializer,
    )


class OrderContainer(containers.DeclarativeContainer):
    
    order_repository = providers.Factory(OrderRepository)
    
    order_serializer = providers.Factory(OrderSerializer)
    order_create_serializer = providers.Factory(OrderCreateSerializer)
    order_update_serializer = providers.Factory(OrderUpdateSerializer)
    order_status_update_serializer = providers.Factory(OrderStatusUpdateSerializer)
    
    order_service = providers.Factory(
        OrderService,
        repository=order_repository,
        customer_repository=providers.Dependency(),
        product_repository=providers.Dependency(),
        serializer=order_serializer,
        create_serializer=order_create_serializer,
        update_serializer=order_update_serializer,
    )


class MainContainer(containers.DeclarativeContainer):
    
    config = Config()
    
    customer = providers.Container(CustomerContainer)
    product = providers.Container(ProductContainer)
    order = providers.Container(OrderContainer)
    

    order.order_service.add_kwargs(
        customer_repository=customer.customer_repository,
        product_repository=product.product_repository,
    )


container = MainContainer()
