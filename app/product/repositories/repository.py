
from datetime import datetime
from beanie import PydanticObjectId

from app.models.product import Product
from app.product.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    """Repository for product operations."""
    
    async def create(self, product_data: ProductCreate) -> Product:
        """Create a new product."""
        product = Product(**product_data.dict())
        return await product.insert()
    
    async def get_by_id(self, product_id: str) -> Product | None:
        """Get product by ID."""
        try:
            return await Product.get(PydanticObjectId(product_id))
        except Exception:
            return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """Get all products with pagination."""
        return await Product.find_all().skip(skip).limit(limit).to_list()
    
    async def update(self, product_id: str, product_data: ProductUpdate) -> Product | None:
        """Update product."""
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        update_data = product_data.dict(exclude_unset=True)
        if not update_data:
            return product
        
        # Update fields
        for field, value in update_data.items():
            setattr(product, field, value)
        
        product.updated_at = datetime.utcnow()  # Update timestamp
        return await product.save()
    
    async def delete(self, product_id: str) -> bool:
        """Delete product."""
        product = await self.get_by_id(product_id)
        if not product:
            return False
        
        await product.delete()
        return True
    
    async def get_by_ids(self, product_ids: list[str]) -> list[Product]:
        """Get multiple products by IDs."""
        try:
            object_ids = [PydanticObjectId(pid) for pid in product_ids]
            return await Product.find({"_id": {"$in": object_ids}}).to_list()
        except Exception:
            return []
