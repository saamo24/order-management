from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order


class Database:
    
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database() -> Database:
    return db


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.database_name]
    
    await init_beanie(
        database=db.database,
        document_models=[Customer, Product, Order]
    )


async def close_mongo_connection():
    if db.client:
        db.client.close()
