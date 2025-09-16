
from fastapi import APIRouter, Depends, Query

from app.container.dependencies import get_product_service
from app.product.services.service import ProductService
from app.product.schemas.product import ProductCreate, ProductUpdate, ProductResponse


router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """Create a new product."""
    return await service.create_product(product_data)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    """Get product by ID."""
    return await service.get_product_by_id(product_id)

@router.get("/", response_model=list[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    service: ProductService = Depends(get_product_service)
):
    """List all products with pagination."""
    return await service.get_all_products(skip, limit)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    """Update product."""
    return await service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    """Delete product."""
    await service.delete_product(product_id)
