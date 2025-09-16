
from datetime import datetime
from beanie import PydanticObjectId

from app.models.customer import Customer
from app.customer.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:
    """Customer Repository."""
    
    async def create(self, customer_data: CustomerCreate) -> Customer:
        """Create a new customer."""
        customer = Customer(**customer_data.dict())
        return await customer.insert()
    
    async def get_by_id(self, customer_id: str) -> Customer | None:
        """Get customer by ID."""
        try:
            return await Customer.get(PydanticObjectId(customer_id))
        except Exception:
            return None
    
    async def get_by_email(self, email: str) -> Customer | None:
        """Get customer by email."""
        return await Customer.find_one({"email": email})
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        """Get all customers with pagination."""
        return await Customer.find_all().skip(skip).limit(limit).to_list()
    
    async def update(self, customer_id: str, customer_data: CustomerUpdate) -> Customer | None:
        """Update customer."""
        customer = await self.get_by_id(customer_id)
        if not customer:
            return None
        
        update_data = customer_data.dict(exclude_unset=True)
        if not update_data:
            return customer
        
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        customer.updated_at = datetime.utcnow()
        return await customer.save()
    
    async def delete(self, customer_id: str) -> bool:
        """Delete customer."""
        customer = await self.get_by_id(customer_id)
        if not customer:
            return False
        
        await customer.delete()
        return True
