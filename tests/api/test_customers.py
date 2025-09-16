import pytest
from httpx import AsyncClient

from tests.constants import *



@pytest.mark.asyncio
class TestCustomerEndpoints:

    async def test_create_customer_success(self, async_client: AsyncClient):

        customer_data = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        }
        
        response = await async_client.post("/customers/", json=customer_data)
        
        assert response.status_code == CREATED_CODE
        data = response.json()
        assert data["name"] == customer_data["name"]
        assert data["email"] == customer_data["email"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_customer_duplicate_email(self, async_client: AsyncClient, sample_customer):
        customer_data = {
            "name": "Different Name",
            "email": sample_customer.email  # Same email as sample_customer
        }
        
        response = await async_client.post("/customers/", json=customer_data)
        
        assert response.status_code == BAD_REQUEST_CODE

    async def test_create_customer_invalid_email(self, async_client: AsyncClient):
        customer_data = {
            "name": "Test User",
            "email": "invalid-email"
        }
        
        response = await async_client.post("/customers/", json=customer_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_create_customer_missing_fields(self, async_client: AsyncClient):
        """Test customer creation with missing required fields."""
        customer_data = {
            "name": "Test User"
            # Missing email
        }
        
        response = await async_client.post("/customers/", json=customer_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_get_customer_success(self, async_client: AsyncClient, sample_customer):
        """Test successful customer retrieval."""
        response = await async_client.get(f"/customers/{sample_customer.id}")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["id"] == str(sample_customer.id)
        assert data["name"] == sample_customer.name
        assert data["email"] == sample_customer.email

    async def test_get_customer_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.get(f"/customers/{fake_id}")
        
        assert response.status_code == NOT_FOUND_CODE


    async def test_list_customers_with_data(self, async_client: AsyncClient, multiple_customers):
        response = await async_client.get("/customers/")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(multiple_customers)
        


    async def test_update_customer_success(self, async_client: AsyncClient, sample_customer):
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        response = await async_client.put(f"/customers/{sample_customer.id}", json=update_data)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["id"] == str(sample_customer.id)


    async def test_update_customer_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        response = await async_client.put(f"/customers/{fake_id}", json=update_data)
        
        assert response.status_code == NOT_FOUND_CODE

    async def test_update_customer_duplicate_email(self, async_client: AsyncClient, multiple_customers):
        customer1, customer2 = multiple_customers[0], multiple_customers[1]
        update_data = {
            "name": f"{customer1.name} Updated",
            "email": customer2.email  # Try to use customer2's email for customer1
        }
        
        response = await async_client.put(f"/customers/{customer1.id}", json=update_data)
        
        assert response.status_code == BAD_REQUEST_CODE

    async def test_delete_customer_success(self, async_client: AsyncClient, sample_customer):
        response = await async_client.delete(f"/customers/{sample_customer.id}")
        
        assert response.status_code == NO_CONTENT_CODE
        
        get_response = await async_client.get(f"/customers/{sample_customer.id}")
        assert get_response.status_code == NOT_FOUND_CODE

    async def test_delete_customer_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.delete(f"/customers/{fake_id}")
        
        assert response.status_code == NOT_FOUND_CODE

