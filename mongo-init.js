// MongoDB initialization script
db = db.getSiblingDB('order_management');

// Create collections
db.createCollection('customers');
db.createCollection('products');
db.createCollection('orders');

// Create indexes
db.customers.createIndex({ "email": 1 }, { unique: true });
db.products.createIndex({ "name": 1 });
db.orders.createIndex({ "customer_id": 1 });
db.orders.createIndex({ "status": 1 });
db.orders.createIndex({ "created_at": 1 });

print('Database initialized successfully');
