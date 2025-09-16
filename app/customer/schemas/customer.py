from pydantic import BaseModel, EmailStr
from datetime import datetime


class CustomerBase(BaseModel):
    """Base customer schema."""
    name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""
    name: str | None
    email: EmailStr | None


class CustomerResponse(CustomerBase):
    """Schema for customer response."""
    id: str
    created_at: datetime
    updated_at: datetime | None
    
    class Config:
        from_attributes = True
