import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.main import app
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.core.config import settings



@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def mongo_client():
    """Create a MongoDB client for testing."""
    client = AsyncIOMotorClient(settings.mongodb_url)
    yield client
    client.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_db(mongo_client):
    """Create a test database."""
    db_name = f"{settings.database_name}_test"
    db = mongo_client[db_name]
    
    # Initialize Beanie with test database
    await init_beanie(
        database=db,
        document_models=[Customer, Product, Order]
    )

    await db.customers.delete_many({})
    await db.products.delete_many({})
    await db.orders.delete_many({})
    
    yield db

    await db.customers.delete_many({})
    await db.products.delete_many({})
    await db.orders.delete_many({})
    # Cleanup: drop the test database
    await mongo_client.drop_database(db_name)


@pytest_asyncio.fixture
async def async_client(mongo_db):
    """Create an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def sample_customer(mongo_db):
    """Create a sample customer for testing."""
    customer_data = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    customer = Customer(**customer_data)
    await customer.insert()
    
    yield customer
    
    # Cleanup
    await customer.delete()


@pytest_asyncio.fixture
async def sample_product(mongo_db):
    """Create a sample product for testing."""
    product_data = {
        "name": "Test Product",
        "price": 29.99
    }
    product = Product(**product_data)
    await product.insert()
    
    yield product
    
    # Cleanup
    await product.delete()


@pytest_asyncio.fixture
async def sample_order(mongo_db, sample_customer, sample_product):
    """Create a sample order for testing."""
    from app.models.order import OrderItem
    
    order_data = {
        "customer_id": str(sample_customer.id),
        "customer_name": sample_customer.name,
        "customer_email": sample_customer.email,
        "items": [
            OrderItem(
                product_id=str(sample_product.id),
                product_name=sample_product.name,
                quantity=2,
                unit_price=sample_product.price
            )
        ]
    }
    order = Order(**order_data)
    await order.insert()
    
    yield order
    
    # Cleanup
    await order.delete()


@pytest_asyncio.fixture
async def multiple_customers(mongo_db):
    """Create multiple customers for testing."""
    # Clear before insert
    await mongo_db.customers.delete_many({})

    customers_data = [
        {"name": "Alice Smith", "email": "alice@example.com"},
        {"name": "Bob Johnson", "email": "bob@example.com"},
        {"name": "Charlie Brown", "email": "charlie@example.com"},
    ]
    
    customers = []
    for data in customers_data:
        customer = Customer(**data)
        await customer.insert()
        customers.append(customer)
    
    yield customers
    
    # Cleanup
    for customer in customers:
        await customer.delete()


@pytest_asyncio.fixture
async def multiple_products(mongo_db):
    # Clear before insert
    await mongo_db.products.delete_many({})
    
    """Create multiple products for testing."""
    products_data = [
        {"name": "Laptop", "price": 999.99},
        {"name": "Mouse", "price": 25.50},
        {"name": "Keyboard", "price": 75.00},
    ]
    
    products = []
    for data in products_data:
        product = Product(**data)
        await product.insert()
        products.append(product)
    
    yield products
    
    # Cleanup
    await mongo_db.products.delete_many({})

