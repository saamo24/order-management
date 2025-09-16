from fastapi import APIRouter, Depends, status, Query

from app.container.dependencies import get_customer_service
from app.customer.services.service import CustomerService
from app.customer.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    """Create a new customer."""
    return await service.create_customer(customer_data)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """Get customer by ID."""
    return await service.get_customer_by_id(customer_id)


@router.get("/", response_model=list[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0, description="Number of customers to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of customers to return"),
    service: CustomerService = Depends(get_customer_service)
):
    """List all customers with pagination."""
    return await service.get_all_customers(skip, limit)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_data: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service)
):
    """Update customer."""
    return await service.update_customer(customer_id, customer_data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """Delete customer."""
    await service.delete_customer(customer_id)
