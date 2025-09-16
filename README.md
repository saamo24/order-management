# 🛒 Order Management API

A modern, scalable FastAPI-based microservice for managing orders, customers, and products. Built with clean architecture principles, dependency injection, and MongoDB for data persistence.

## ✨ Features

- **FastAPI** with automatic OpenAPI documentation
- **MongoDB** integration with Beanie ODM
- **Dependency Injection** using dependency-injector
- **Clean Architecture** with separated layers (routes, services, repositories)
- **Docker** containerization with multi-environment support
- **Comprehensive Testing** with pytest and async support
- **CORS** enabled for frontend integration
- **Health Checks** for monitoring

## 🔧 Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **MongoDB**

## 🚀 Installation

### Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/saamo24/order-management.git
   cd order-management
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start services**
   ```bash
   make build
   make up
   ```

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**
   - Install MongoDB locally or use Docker:
     ```bash
     docker run -d -p 27017:27017 --name mongodb mongo:7.0
     ```

## 🏃‍♂️ Running the Project

### Development Mode (with hot reload)

```bash
# Using Docker
make dev

# Using local Python
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Using Docker
make up

# Using local Python
python -m app.main
```

### Access Points

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **MongoDB Admin**: http://localhost:8081 (admin/admin)

## 📖 Usage Examples

### Create a Customer

```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

### Create a Product

```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
  }'
```

### Create an Order

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer_id_here",
    "items": [
      {
        "product_id": "product_id_here",
        "quantity": 2,
      }
    ]
  }'
```

### Get All Orders

```bash
curl -X GET "http://localhost:8000/orders/"
```

## 🧪 Testing

### Run Tests

```bash
# Using Docker
make run-tests

# Using local Python
pytest tests/ -v
```

### Run Tests with Coverage

```bash
# Using Docker
make run-tests-coverage

# Using local Python
pytest tests/ --cov=app --cov-report=html
```

### Test Database Setup

```bash
# Create test database
make create-test-db

# Drop test database
make drop-test-db
```

## 📁 Project Structure

```
order-management/
├── app/                          # Main application package
│   ├── container/               # Dependency injection container
│   │   ├── config.py            # Container configuration
│   │   ├── container.py         # Main container setup
│   │   └── dependencies.py      # Dependency definitions
│   ├── core/                    # Core application components
│   │   ├── config.py            # Application settings
│   │   ├── database.py          # Database connection
│   │   └── serializers/         # Base serializers
│   ├── customer/                # Customer domain
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access layer
│   │   ├── schemas/             # Pydantic models
│   │   └── serializers/         # Data serialization
│   ├── product/                 # Product domain
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access layer
│   │   ├── schemas/             # Pydantic models
│   │   └── serializers/         # Data serialization
│   ├── order/                   # Order domain
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access layer
│   │   ├── schemas/             # Pydantic models
│   │   └── serializers/         # Data serialization
│   ├── models/                  # Database models
│   └── main.py                  # Application entry point
├── tests/                       # Test suite
│   ├── api/                     # API integration tests
│   ├── conftest.py              # Test configuration
│   └── constants.py             # Test constants
├── docker-compose.yml           # Production Docker setup
├── docker-compose.dev.yml       # Development Docker setup
├── Dockerfile                   # Application container
├── Makefile                     # Development commands
├── requirements.txt             # Python dependencies
├── pytest.ini                  # Test configuration
└── README.md                   # This file
```

## 📚 API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The API provides endpoints for:

- **Customers**: CRUD operations for customer management
- **Products**: CRUD operations for product catalog
- **Orders**: Order creation, status updates, and retrieval

---