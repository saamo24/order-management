
from beanie import Document
from pydantic import Field, field_validator
from datetime import datetime


class Product(Document):
    """Product model."""
    
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "products"
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        """Validate that price is greater than 0."""
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v
