# Makefile for Order Management Docker operations

.PHONY: help build up down dev logs clean restart status

# Database management
DB_NAME=order_management_test
DB_USER=admin
DB_PASSWORD=password
ADMIN_DB=admin

exec-db = docker compose exec -T mongodb mongosh --username $(DB_USER) --password $(DB_PASSWORD) --authenticationDatabase $(ADMIN_DB) --eval

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services (production)"
	@echo "  dev       - Start all services (development with hot reload)"
	@echo "  down      - Stop all services"
	@echo "  logs      - Show logs for all services"
	@echo "  logs-app  - Show logs for app service only"
	@echo "  logs-db   - Show logs for MongoDB service only"
	@echo "  restart   - Restart all services"
	@echo "  status    - Show status of all services"
	@echo "  clean     - Remove all containers, networks, and volumes"
	@echo "  shell     - Open shell in app container"
	@echo "  test      - Run tests in container"
	@echo ""
	@echo "Database management:"
	@echo "  create-test-db    - Create test database with collections and indexes"
	@echo "  drop-test-db      - Drop test database"
	@echo "  run-tests         - Run tests with test database"
	@echo "  run-tests-coverage - Run tests with coverage report"

# Build Docker images
build:
	docker-compose build

# Start all services (production)
up:
	docker-compose up -d

# Start all services (development)
dev:
	docker-compose -f docker-compose.dev.yml up -d

# Stop all services
down:
	docker-compose down

# Stop development services
dev-down:
	docker-compose -f docker-compose.dev.yml down

# Show logs for all services
logs:
	docker-compose logs -f

# Show logs for app service
logs-app:
	docker-compose logs -f app

# Show logs for MongoDB service
logs-db:
	docker-compose logs -f mongodb

# Show development logs
dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Restart all services
restart:
	docker-compose restart

# Show status of all services
status:
	docker-compose ps

# Show development status
dev-status:
	docker-compose -f docker-compose.dev.yml ps

# Clean up everything
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Open shell in app container
shell:
	docker-compose exec app /bin/bash

# Open shell in development app container
dev-shell:
	docker-compose -f docker-compose.dev.yml exec app /bin/bash

# Install dependencies
install:
	docker-compose exec app pip install -r requirements.txt

# Install development dependencies
dev-install:
	docker-compose -f docker-compose.dev.yml exec app pip install -r requirements.txt

# Database management commands
create-test-db:
	@echo "Starting database service..."
	docker compose -f docker-compose.dev.yml up -d mongodb
	@echo "Waiting for database to be ready..."
	@until docker compose -f docker-compose.dev.yml exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do \
		echo "Waiting for database..."; \
		sleep 2; \
	done
	$(exec-db) "db = db.getSiblingDB('$(DB_NAME)'); db.dropDatabase();"
	$(exec-db) "db = db.getSiblingDB('$(DB_NAME)'); db.createCollection('customers'); db.createCollection('products'); db.createCollection('orders');"
	$(exec-db) "db = db.getSiblingDB('$(DB_NAME)'); db.customers.createIndex({ 'email': 1 }, { unique: true }); db.products.createIndex({ 'name': 1 }); db.orders.createIndex({ 'customer_id': 1 }); db.orders.createIndex({ 'status': 1 }); db.orders.createIndex({ 'created_at': 1 });"
	@echo "Test database $(DB_NAME) created successfully"

drop-test-db:
	@echo "Dropping test database..."
	$(exec-db) "db = db.getSiblingDB('$(DB_NAME)'); db.dropDatabase();"
	@echo "Test database $(DB_NAME) dropped successfully"

run-tests:
	docker compose -f docker-compose.dev.yml run --rm -e DATABASE_NAME=$(DB_NAME) -e MONGODB_URL=mongodb://$(DB_USER):$(DB_PASSWORD)@mongodb:27017/$(DB_NAME)?authSource=$(ADMIN_DB) app python -m pytest tests/ -v
