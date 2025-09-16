import pytest
from httpx import AsyncClient

from tests.constants import *


@pytest.mark.asyncio
class TestProductEndpoints:

    async def test_create_product_success(self, async_client: AsyncClient):
        product_data = {
            "name": "Wireless Headphones",
            "price": 149.99
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == CREATED_CODE
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["price"] == product_data["price"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_product_invalid_price(self, async_client: AsyncClient):
        product_data = {
            "name": "Test Product",
            "price": -10.0  # Invalid negative price
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_create_product_zero_price(self, async_client: AsyncClient):
        product_data = {
            "name": "Free Product",
            "price": 0.0  # Invalid zero price
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_create_product_missing_fields(self, async_client: AsyncClient):
        product_data = {
            "name": "Test Product"
            # Missing price
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_create_product_empty_name(self, async_client: AsyncClient):
        product_data = {
            "name": "",  # Empty name
            "price": 29.99
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_create_product_long_name(self, async_client: AsyncClient):
        product_data = {
            "name": "A" * 201,  # Exceeds max_length=200
            "price": 29.99
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_get_product_success(self, async_client: AsyncClient, sample_product):
        response = await async_client.get(f"/products/{sample_product.id}")

        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["id"] == str(sample_product.id)
        assert data["name"] == sample_product.name
        assert data["price"] == sample_product.price

    async def test_get_product_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.get(f"/products/{fake_id}")
        
        assert response.status_code == NOT_FOUND_CODE


    async def test_list_products_with_data(self, async_client: AsyncClient, multiple_products):
        response = await async_client.get("/products/")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(multiple_products)


    async def test_list_products_pagination(self, async_client: AsyncClient, multiple_products):
        # Test skip parameter
        response = await async_client.get("/products/?skip=1")
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert len(data) == len(multiple_products) - 1
        
        # Test limit parameter
        response = await async_client.get("/products/?limit=2")
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert len(data) == 2
        
        # Test both skip and limit
        response = await async_client.get("/products/?skip=1&limit=1")
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert len(data) == 1

    async def test_update_product_success(self, async_client: AsyncClient, sample_product):
        update_data = {
            "name": "Updated Product Name",
            "price": 199.99
        }
        
        response = await async_client.put(f"/products/{sample_product.id}", json=update_data)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["price"] == update_data["price"]
        assert data["id"] == str(sample_product.id)

    async def test_update_product_partial(self, async_client: AsyncClient, sample_product):
        update_data = {
            "name": "Partially Updated Name"
            # Only updating name, not price
        }
        
        response = await async_client.put(f"/products/{sample_product.id}", json=update_data)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["price"] == sample_product.price  # Price should remain unchanged

    async def test_update_product_price_only(self, async_client: AsyncClient, sample_product):
        update_data = {
            "price": 299.99
        }
        
        response = await async_client.put(f"/products/{sample_product.id}", json=update_data)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["price"] == update_data["price"]
        assert data["name"] == sample_product.name  # Name should remain unchanged

    async def test_update_product_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        update_data = {
            "name": "Updated Name"
        }
        
        response = await async_client.put(f"/products/{fake_id}", json=update_data)
        
        assert response.status_code == NOT_FOUND_CODE

    async def test_update_product_invalid_price(self, async_client: AsyncClient, sample_product):
        update_data = {
            "price": -50.0  # Invalid negative price
        }
        
        response = await async_client.put(f"/products/{sample_product.id}", json=update_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_update_product_invalid_name(self, async_client: AsyncClient, sample_product):
        update_data = {
            "name": ""  # Empty name
        }
        
        response = await async_client.put(f"/products/{sample_product.id}", json=update_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_delete_product_success(self, async_client: AsyncClient, sample_product):
        response = await async_client.delete(f"/products/{sample_product.id}")
        
        assert response.status_code == NO_CONTENT_CODE
        
        get_response = await async_client.get(f"/products/{sample_product.id}")
        assert get_response.status_code == NOT_FOUND_CODE

    async def test_delete_product_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.delete(f"/products/{fake_id}")
        
        assert response.status_code == NOT_FOUND_CODE


    async def test_product_price_precision(self, async_client: AsyncClient):
        product_data = {
            "name": "Precision Product",
            "price": 99.999  # Test decimal precision
        }
        
        response = await async_client.post("/products/", json=product_data)
        
        assert response.status_code == CREATED_CODE
        data = response.json()
        assert data["price"] == 99.999
