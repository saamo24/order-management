
from app.core.serializers.base import BaseSerializer
from app.models.product import Product
from app.product.schemas.product import ProductCreate, ProductUpdate, ProductResponse


class ProductSerializer(BaseSerializer[Product, ProductResponse]):
    """Serializer for Product domain model."""
    
    async def serialize(self, product: Product) -> ProductResponse:
        """Serialize Product to ProductResponse."""
        return ProductResponse(
            id=str(product.id),
            name=product.name,
            price=product.price,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    
    async def serialize_for_list(self, products: list[Product]) -> list[ProductResponse]:
        """Serialize list of products."""
        return [await self.serialize(product) for product in products]


class ProductCreateSerializer(BaseSerializer[ProductCreate, ProductResponse]):
    """Serializer for ProductCreate operations."""
    
    async def serialize(self, data: ProductCreate) -> ProductResponse:
        """Serialize ProductCreate to dictionary."""
        return ProductResponse(
            id=str(data.id),
            name=data.name,
            price=data.price,
            created_at=data.created_at,
            updated_at=data.updated_at
        )


class ProductUpdateSerializer(BaseSerializer[ProductUpdate, ProductResponse]):
    """Serializer for ProductUpdate operations."""
    
    async def serialize(self, data: ProductUpdate) -> ProductResponse:
        """Serialize ProductUpdate to dictionary."""
        return ProductResponse(
            id=str(data.id),
            name=data.name,
            price=data.price,
            created_at=data.created_at,
            updated_at=data.updated_at
        )
