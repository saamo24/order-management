from fastapi import HTTPException, status

from app.product.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.product.serializers.serializer import (
    ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer
)
from app.product.repositories.repository import ProductRepository
    

class ProductService:
    """Service for product business logic."""
    
    def __init__(
        self, 
        repository: ProductRepository,
        serializer: ProductSerializer,
        create_serializer: ProductCreateSerializer,
        update_serializer: ProductUpdateSerializer
    ):
        self.repository = repository
        self.serializer = serializer
        self.create_serializer = create_serializer
        self.update_serializer = update_serializer
    
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product with business validation."""
        product = await self.repository.create(product_data)
        return await self.serializer.serialize(product)
    
    async def get_product_by_id(self, product_id: str) -> ProductResponse:
        """Get product by ID."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return await self.serializer.serialize(product)
    
    async def get_all_products(self, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Get all products with pagination."""
        products = await self.repository.get_all(skip, limit)
        return await self.serializer.serialize_for_list(products)
    
    async def update_product(self, product_id: str, product_data: ProductUpdate) -> ProductResponse:
        """Update product with business validation."""
        # Check if product exists
        existing_product = await self.repository.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        updated_product = await self.repository.update(product_id, product_data)
        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update product"
            )
        
        return await self.serializer.serialize(updated_product)
    
    async def delete_product(self, product_id: str) -> bool:
        """Delete product."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return await self.repository.delete(product_id)
    
    async def get_products_by_ids(self, product_ids: list[str]) -> list[ProductResponse]:
        """Get multiple products by IDs."""
        return await self.repository.get_by_ids(product_ids)
