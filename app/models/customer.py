from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime


class Customer(Document):
    """Customer model."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "customers"
