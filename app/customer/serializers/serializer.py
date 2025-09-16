
from app.core.serializers.base import BaseSerializer
from app.models.customer import Customer
from app.customer.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse


class CustomerSerializer(BaseSerializer[Customer, CustomerResponse]):
    """Serializer for Customer."""
    
    async def serialize(self, customer: Customer) -> CustomerResponse:
        """Serialize Customer to CustomerResponse."""
        return CustomerResponse(
            id=str(customer.id),
            name=customer.name,
            email=customer.email,
            created_at=customer.created_at,
            updated_at=customer.updated_at
        )
    

class CustomerCreateSerializer(BaseSerializer[CustomerCreate, CustomerResponse]):
    """Serializer for CustomerCreate."""
    
    async def serialize(self, data: CustomerCreate) -> CustomerResponse:
        """Serialize CustomerCreate to dictionary."""
        return CustomerResponse(
            id=str(data.id),
            name=data.name,
            email=data.email,
            created_at=data.created_at,
            updated_at=data.updated_at
        )
    


class CustomerUpdateSerializer(BaseSerializer[CustomerUpdate, CustomerResponse]):
    """Serializer for CustomerUpdate."""
    
    async def serialize(self, data: CustomerUpdate) -> CustomerResponse:
        """Serialize CustomerUpdate to dictionary."""
        return CustomerResponse(
            id=str(data.id),
            name=data.name,
            email=data.email,
            created_at=data.created_at,
            updated_at=data.updated_at
        )
    
