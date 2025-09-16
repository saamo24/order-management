
from fastapi import HTTPException, status

from app.models.customer import Customer
from app.customer.repositories.repository import CustomerRepository
from app.customer.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.customer.serializers.serializer import (
    CustomerSerializer, CustomerCreateSerializer, CustomerUpdateSerializer
)


class CustomerService:
    """Service for customer business logic."""
    
    def __init__(
        self, 
        repository: CustomerRepository,
        serializer: CustomerSerializer,
        create_serializer: CustomerCreateSerializer,
        update_serializer: CustomerUpdateSerializer
    ):
        self.repository = repository
        self.serializer = serializer
        self.create_serializer = create_serializer
        self.update_serializer = update_serializer
    
    async def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """Create a new customer with business validation."""
        existing_customer = await self.repository.get_by_email(customer_data.email)
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this email already exists"
            )
        
        customer = await self.repository.create(customer_data)
        
        return await self.serializer.serialize(customer)
    
    async def get_customer_by_id(self, customer_id: str) -> CustomerResponse:
        """Get customer by ID."""
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        return await self.serializer.serialize(customer)
    
    async def get_customer_by_email(self, email: str) -> Customer | None:
        """Get customer by email."""
        return await self.repository.get_by_email(email)
    
    async def get_all_customers(self, skip: int = 0, limit: int = 100) -> list[CustomerResponse]:
        """Get all customers with pagination."""
        customers = await self.repository.get_all(skip, limit)
        return await self.serializer.serialize_list(customers)
    
    async def update_customer(self, customer_id: str, customer_data: CustomerUpdate) -> CustomerResponse:
        """Update customer with business validation."""
        existing_customer = await self.repository.get_by_id(customer_id)
        if not existing_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        if customer_data.email and customer_data.email != existing_customer.email:
            email_exists = await self.repository.get_by_email(customer_data.email)
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Customer with this email already exists"
                )
        
        updated_customer = await self.repository.update(customer_id, customer_data)
        if not updated_customer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update customer"
            )
        
        return await self.serializer.serialize(updated_customer)
    
    async def delete_customer(self, customer_id: str) -> bool:
        """Delete customer."""
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        return await self.repository.delete(customer_id)
