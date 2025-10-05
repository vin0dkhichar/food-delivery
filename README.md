# Food Delivery Platform

A **microservices-based Food Delivery Platform** built with **FastAPI**, **Kafka**, **PostgreSQL**, and **Elasticsearch**.

## Architecture Overview

This platform consists of three main services:

- **User Service:** Manages users, restaurants, menu items, file uploads, and search functionality
- **Order Service:** Handles order creation, tracking, and status updates
- **Notification Service:** Sends email/SMS notifications via Kafka events

### Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Message Broker**: Apache Kafka
- **Search Engine**: Elasticsearch
- **File Storage**: MinIo
- **Email**: MailerSend
- **SMS**: Twilio
- **Authentication**: JWT with OAuth2
- **Reverse Proxy**: Nginx

## Prerequisites

- Python
- PostgreSQL
- Apache Kafka
- Elasticsearch
- Nginx
- MinIO

## Setup

### 1. Elasticsearch Installation

Install Elasticsearch on Ubuntu/Debian:

```bash
# Install prerequisites
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg

# Add Elasticsearch GPG key
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | \
  sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# Add Elasticsearch repository
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] \
https://artifacts.elastic.co/packages/8.x/apt stable main" | \
  sudo tee /etc/apt/sources.list.d/elastic-8.x.list

# Install Elasticsearch
sudo apt update
sudo apt install -y elasticsearch

# Enable and start Elasticsearch
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl status elasticsearch
```

#### Reset Elasticsearch Password

```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```

Save the generated password for use in your `.env` file.

#### Verify Elasticsearch is Running

```bash
# Test connection
curl -k -u elastic:YOUR_PASSWORD -X GET "https://localhost:9200"
```

#### Create Elasticsearch Indices

Run these commands to create the required indices:

```bash
# Delete existing indices (if needed)
curl -X DELETE "https://localhost:9200/restaurants" \
  -u elastic:YOUR_PASSWORD -k

curl -X DELETE "https://localhost:9200/menu_items" \
  -u elastic:YOUR_PASSWORD -k

# Create restaurants index with mappings
curl -X PUT "https://localhost:9200/restaurants" \
  -u elastic:YOUR_PASSWORD \
  -H 'Content-Type: application/json' \
  -d '{
    "mappings": {
      "properties": {
        "name": { "type": "text" },
        "description": { "type": "text" },
        "address": { "type": "text" },
        "category": { "type": "keyword" },
        "cuisine_type": { "type": "keyword" },
        "tags": { "type": "keyword" },
        "location": { "type": "geo_point" }
      }
    }
  }' -k

# Create menu_items index with mappings
curl -X PUT "https://localhost:9200/menu_items" \
  -u elastic:YOUR_PASSWORD \
  -H 'Content-Type: application/json' \
  -d '{
    "mappings": {
      "properties": {
        "name": { "type": "text" },
        "description": { "type": "text" },
        "price": { "type": "float" },
        "is_available": { "type": "boolean" },
        "category": { "type": "keyword" },
        "cuisine_type": { "type": "keyword" },
        "tags": { "type": "keyword" },
        "restaurant_id": { "type": "integer" }
      }
    }
  }' -k
```

### 2. Apache Kafka Installation

Download and set up Kafka:

```bash
# Download Kafka
wget https://archive.apache.org/dist/kafka/4.1.0/kafka_2.13-4.1.0.tgz
tar -xzf kafka_2.13-4.1.0.tgz
cd kafka_2.13-4.1.0

# Create data directory
mkdir -p ~/kafka-data
```

#### Configure Kafka

Edit the Kafka configuration:

```bash
nano config/server.properties
```

Update the log directory:

```properties
log.dirs=/home/your-username/kafka-data
```

#### Format and Start Kafka

```bash
# Generate a cluster ID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# Format the storage directory
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties

# Start Kafka server
bin/kafka-server-start.sh config/server.properties
```

#### Create Kafka Topics

```bash
# Create the orders topic
bin/kafka-topics.sh --create \
  --topic orders \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

#### Verify Kafka is Running

```bash
# List topics
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Test producer
bin/kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092

# Test consumer (in another terminal)
bin/kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092
```

### 3. MinIO Installation

Download and install MinIO:

```bash
# Download MinIO .deb package
wget https://dl.min.io/server/minio/release/linux-amd64/minio.deb

# Install MinIO
sudo dpkg -i minio.deb

# Create data directory
mkdir -p ~/minio/data
```

#### Configure MinIO Credentials

Add MinIO credentials to your `.bashrc`:

```bash
nano ~/.bashrc
```

Add these lines:

```bash
# MinIO Configuration
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin123
```

Apply changes:

```bash
source ~/.bashrc
```

#### Start MinIO Server

```bash
minio server ~/minio/data
```

#### Configure MinIO in User Service

Access the MinIO Console:

1. Login with credentials (minioadmin/minioadmin123)
2. Create a bucket (e.g., `menu-items`)
3. Set bucket policy to public
4. Add a Storage Backend record in your database:

```sql
INSERT INTO storage_backend (
  name, 
  backend_type, 
  aws_host, 
  aws_bucket, 
  aws_access_key_id, 
  aws_secret_access_key, 
  aws_region, 
  active
) VALUES (
  'MinIO Local',
  'amazon_s3',
  'http://localhost:9000',
  'food-delivery-uploads',
  'minioadmin',
  'minioadmin123',
  'ap-south-1',
  true
);
```

## Environment Variables

### User Service (.env)

```env
DATABASE_URL=postgresql+psycopg2://postgres:admin@localhost:5432/userdb
SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

ELASTICSEARCH_URL=https://localhost:9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=elsaticpass
```

### Order Service (.env)

```env
DATABASE_URL=postgresql+psycopg2://postgres:admin@localhost:5432/orderdb

SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

KAFKA_BROKER=localhost:9092
KAFKA_TOPIC_ORDERS=orders
```

### Notification Service (.env)

```env
KAFKA_BROKER=localhost:9092

KAFKA_TOPIC_ORDERS=orders

GROUP_ID=notification_service

MAILERSEND_API_KEY=api_key
EMAIL_FROM=email_from

TWILIO_ACCOUNT_SID=acc_sid
TWILIO_AUTH_TOKEN=auth_token
TWILIO_PHONE_NUMBER=phone_number
```

## Running Services Locally

Each service runs independently on different ports:

- **User Service:** `http://127.0.0.1:8001`
- **Order Service:** `http://127.0.0.1:8002`
- **Notification Service:** Background Kafka worker

### User Service

```bash
cd user-service

python3.12 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Order Service

```bash
cd order-service

python3.12 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

### Notification Service (Worker)

```bash
cd notification-service

python3.12 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python3 -m app.worker
```

## API Endpoints

### User Service (`/v1`)

#### Authentication
- `POST /users/` - Register a new user
- `POST /users/login` - Login and get JWT token
- `GET /users/me` - Get current user profile

#### Restaurants
- `POST /restaurants/` - Create a restaurant
- `GET /restaurants/{id}` - Get restaurant details
- `GET /restaurants/` - List all restaurants

#### Menu Items
- `POST /menu-items/` - Create a menu item (Restaurant owner only)
- `GET /menu-items/{id}` - Get menu item details
- `GET /menu-items/restaurant/{restaurant_id}` - List menu items by restaurant

#### File Upload
- `POST /files/upload` - Upload an image to MinIo
- `GET /files/{file_id}` - Get file details

#### Search
- `GET /search/restaurants?q={query}` - Search restaurants.
- `GET /search/menu-items?q={query}` - Search menu items
- `GET /search/restaurants/nearby?lat={lat}&lon={lon}&distance={distance}` - Find nearby restaurants

### Order Service (`/v1/orders`)

- `POST /orders/` - Create a new order
- `GET /orders/` - List user's orders
- `GET /orders/{order_id}` - Get order details
- `PUT /orders/{order_id}/status` - Update order status


## Authentication Flow

1. User registers via `POST /v1/users/`
2. User logs in via `POST /v1/users/login` to receive a JWT token
3. Include the token in subsequent requests: `Authorization: Bearer <token>`
4. The token contains user info (id, email, role, etc.)

## Kafka Event Flow

When an order is created or updated, the Order Service publishes an event to Kafka:

```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "order_id": 123,
  "subject": "Order Confirmation - #123",
  "message": "Thank you for your order..."
}
```

The Notification Service consumes these events and sends:
- Email notification via MailerSend
- SMS notification via Twilio

## Elasticsearch Integration

The User Service indexes restaurants and menu items in Elasticsearch for fast full-text search:

- **Restaurants Index**: name, description, address, category, cuisine_type, tags, geo-location
- **Menu Items Index**: name, description, category, cuisine_type, tags, price

## Nginx Reverse Proxy Setup

Use Nginx to expose all services under a single domain.

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 2. Create Configuration File

```bash
sudo nano /etc/nginx/sites-available/food-delivery-api.conf
```

```nginx
server {
    listen 80;
    server_name food.delivery.my;

    # Health check endpoint
    location /health {
        return 200 "OK";
        add_header Content-Type text/plain;
    }

    # User Service (everything under /v1/users/, /v1/restaurants/, /v1/menu-items/, /v1/search/, /v1/files/)
    location /v1/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Order Service (all /v1/orders/ routes)
    location /v1/orders/ {
        proxy_pass http://127.0.0.1:8002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Enable and Reload

```bash
sudo ln -sf /etc/nginx/sites-available/food-delivery-api.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx reload
```

## API Documentation

FastAPI provides interactive API documentation:

- **User Service Swagger UI** → `http://localhost:8001/docs` or `http://food.delivery.my/v1/docs`
- **Order Service Swagger UI** → `http://localhost:8002/docs` or `http://food.delivery.my/v1/orders/docs`
- **Health Check** → `http://food.delivery.my/health`
