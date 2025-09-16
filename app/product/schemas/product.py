from pydantic import BaseModel, Field
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: str | None = Field(None, min_length=1, max_length=200)
    price: float | None = Field(None, gt=0)


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: str
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True
