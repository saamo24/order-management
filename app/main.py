from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.container.containers import container
from app.customer.routes import customers
from app.product.routes import products
from app.order.routes import orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await connect_to_mongo()

    # Initialize DI container
    container.wire(
        modules=[
            "app.customer.routes.customers",
            "app.product.routes.products",
            "app.order.routes.orders",
        ]
    )
    app.state.container = container

    yield

    # Shutdown
    await close_mongo_connection()
    container.unwire()


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Order Management API",
        "version": settings.api_version,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
