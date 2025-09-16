from app.container.containers import container
from app.customer.services.service import CustomerService
from app.product.services.service import ProductService
from app.order.services.service import OrderService
from app.customer.serializers.serializer import CustomerSerializer
from app.product.serializers.serializer import ProductSerializer
from app.order.serializers.serializer import OrderSerializer


def get_customer_service() -> CustomerService:
    return container.customer.customer_service()


def get_product_service() -> ProductService:
    return container.product.product_service()


def get_order_service() -> OrderService:
    return container.order.order_service()


def get_customer_serializer() -> CustomerSerializer:
    return container.customer.customer_serializer()


def get_product_serializer() -> ProductSerializer:
    return container.product.product_serializer()


def get_order_serializer() -> OrderSerializer:
    return container.order.order_serializer()
