import pytest
from httpx import AsyncClient
from app.models.order import OrderStatus
from tests.constants import *

@pytest.mark.asyncio
class TestOrderEndpoints:

    async def test_create_order_success(self, async_client: AsyncClient, sample_customer, sample_product):
        order_data = {
            "customer_id": str(sample_customer.id),
            "items": [
                {
                    "product_id": str(sample_product.id),
                    "quantity": 2
                }
            ]
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == CREATED_CODE
        data = response.json()
        assert data["customer_id"] == str(sample_customer.id)
        assert data["customer_name"] == sample_customer.name
        assert data["customer_email"] == sample_customer.email
        assert data["status"] == OrderStatus.PENDING
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == str(sample_product.id)
        assert data["items"][0]["product_name"] == sample_product.name
        assert data["items"][0]["quantity"] == 2
        assert data["items"][0]["unit_price"] == sample_product.price
        assert data["total_price"] == 2 * sample_product.price
        assert "id" in data
        assert "created_at" in data

    async def test_create_order_multiple_items(self, async_client: AsyncClient, sample_customer, multiple_products):
        order_data = {
            "customer_id": str(sample_customer.id),
            "items": [
                {
                    "product_id": str(multiple_products[0].id),
                    "quantity": 1
                },
                {
                    "product_id": str(multiple_products[1].id),
                    "quantity": 3
                }
            ]
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == CREATED_CODE
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total_price"] == multiple_products[0].price + (3 * multiple_products[1].price)

    async def test_create_order_empty_items(self, async_client: AsyncClient, sample_customer):
        order_data = {
            "customer_id": str(sample_customer.id),
            "items": []  # Empty items list
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_create_order_invalid_customer(self, async_client: AsyncClient, sample_product):
        order_data = {
            "customer_id": "507f1f77bcf86cd799439011",  # Non-existent customer
            "items": [
                {
                    "product_id": str(sample_product.id),
                    "quantity": 1
                }
            ]
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == NOT_FOUND_CODE

    async def test_create_order_invalid_product(self, async_client: AsyncClient, sample_customer):
        order_data = {
            "customer_id": str(sample_customer.id),
            "items": [
                {
                    "product_id": "507f1f77bcf86cd799439011",  # Non-existent product
                    "quantity": 1
                }
            ]
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == BAD_REQUEST_CODE

    async def test_create_order_invalid_quantity(self, async_client: AsyncClient, sample_customer, sample_product):
        order_data = {
            "customer_id": str(sample_customer.id),
            "items": [
                {
                    "product_id": str(sample_product.id),
                    "quantity": 0  # Invalid quantity
                }
            ]
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_get_order_success(self, async_client: AsyncClient, sample_order):
        response = await async_client.get(f"/orders/{sample_order.id}")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["id"] == str(sample_order.id)
        assert data["customer_id"] == sample_order.customer_id
        assert data["status"] == sample_order.status
        assert len(data["items"]) == len(sample_order.items)

    async def test_get_order_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.get(f"/orders/{fake_id}")
        
        assert response.status_code == NOT_FOUND_CODE


    async def test_list_orders_with_data(self, async_client: AsyncClient, sample_order):
        response = await async_client.get("/orders/")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert isinstance(data, list)
        assert data[-1]["id"] == str(sample_order.id)


    async def test_list_orders_by_customer(self, async_client: AsyncClient, sample_customer, sample_order):
        response = await async_client.get(f"/orders/customer/{sample_customer.id}")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["customer_id"] == str(sample_customer.id)

    async def test_list_orders_by_customer_not_found(self, async_client: AsyncClient):
        fake_customer_id = "507f1f77bcf86cd799439011"
        response = await async_client.get(f"/orders/customer/{fake_customer_id}")
        
        assert response.status_code == NOT_FOUND_CODE

    async def test_list_orders_by_status(self, async_client: AsyncClient, sample_order):
        response = await async_client.get(f"/orders/status/{sample_order.status.value}")
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert isinstance(data, list)
        assert data[-1]["status"] == sample_order.status

    async def test_list_orders_by_status_empty(self, async_client: AsyncClient):
        response = await async_client.get("/orders/status/PAID")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_update_order_status_pending_to_paid(self, async_client: AsyncClient, sample_order):
        status_update = {
            "status": OrderStatus.PAID
        }
        
        response = await async_client.patch(f"/orders/{sample_order.id}/status", json=status_update)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["status"] == OrderStatus.PAID

    async def test_update_order_status_pending_to_cancelled(self, async_client: AsyncClient, sample_order):
        status_update = {
            "status": OrderStatus.CANCELLED
        }
        
        response = await async_client.patch(f"/orders/{sample_order.id}/status", json=status_update)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["status"] == OrderStatus.CANCELLED

    async def test_update_order_status_paid_to_cancelled(self, async_client: AsyncClient, sample_order):
        # First set status to PAID
        await async_client.patch(f"/orders/{sample_order.id}/status", json={"status": OrderStatus.PAID})
        
        # Then try to cancel
        status_update = {
            "status": OrderStatus.CANCELLED
        }
        
        response = await async_client.patch(f"/orders/{sample_order.id}/status", json=status_update)
        
        assert response.status_code == SUCCESS_CODE
        data = response.json()
        assert data["status"] == OrderStatus.CANCELLED

    async def test_update_order_status_invalid_transition(self, async_client: AsyncClient, sample_order):
        # First set status to PAID
        await async_client.patch(f"/orders/{sample_order.id}/status", json={"status": OrderStatus.PAID})
        
        # Then try to go back to PENDING (invalid)
        status_update = {
            "status": OrderStatus.PENDING
        }
        
        response = await async_client.patch(f"/orders/{sample_order.id}/status", json=status_update)
        
        assert response.status_code == BAD_REQUEST_CODE

    async def test_update_order_status_cancelled_to_any(self, async_client: AsyncClient, sample_order):
        # First set status to CANCELLED
        await async_client.patch(f"/orders/{sample_order.id}/status", json={"status": OrderStatus.CANCELLED})
        
        # Then try to change to PAID (invalid)
        status_update = {
            "status": OrderStatus.PAID
        }
        
        response = await async_client.patch(f"/orders/{sample_order.id}/status", json=status_update)
        
        assert response.status_code == BAD_REQUEST_CODE

    async def test_update_order_status_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        status_update = {
            "status": OrderStatus.PAID
        }
        
        response = await async_client.patch(f"/orders/{fake_id}/status", json=status_update)
        
        assert response.status_code == NOT_FOUND_CODE

    async def test_update_order_status_invalid_status(self, async_client: AsyncClient, sample_order):
        status_update = {
            "status": "INVALID_STATUS"
        }
        
        response = await async_client.patch(f"/orders/{sample_order.id}/status", json=status_update)
        
        assert response.status_code == VALIDATION_ERROR_CODE

    async def test_delete_order_success(self, async_client: AsyncClient, sample_order):
        response = await async_client.delete(f"/orders/{sample_order.id}")
        
        assert response.status_code == NO_CONTENT_CODE
        
        get_response = await async_client.get(f"/orders/{sample_order.id}")
        assert get_response.status_code == NOT_FOUND_CODE


    async def test_delete_order_not_found(self, async_client: AsyncClient):
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.delete(f"/orders/{fake_id}")
        
        assert response.status_code == NOT_FOUND_CODE


    async def test_order_total_price_calculation(self, async_client: AsyncClient, sample_customer, multiple_products):
        order_data = {
            "customer_id": str(sample_customer.id),
            "items": [
                {
                    "product_id": str(multiple_products[0].id),
                    "quantity": 2
                },
                {
                    "product_id": str(multiple_products[1].id),
                    "quantity": 1
                }
            ]
        }
        
        response = await async_client.post("/orders/", json=order_data)
        
        assert response.status_code == CREATED_CODE
        data = response.json()
        expected_total = (2 * multiple_products[0].price) + multiple_products[1].price
        assert data["total_price"] == expected_total
        
        assert data["items"][0]["total_price"] == 2 * multiple_products[0].price
        assert data["items"][1]["total_price"] == multiple_products[1].price
