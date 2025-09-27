# Food Delivery Platform

This project is a **microservices-based Food Delivery Platform** built with **FastAPI** and **Kafka**.  
It consists of three main services:

- **User Service** → Manages users, restaurants, and menu items  
- **Order Service** → Handles orders and order status  
- **Notification Service** → Sends email/SMS notifications via Kafka  

## Running Services Locally

Each service runs independently:

- **User Service** → `http://127.0.0.1:8001`  
- **Order Service** → `http://127.0.0.1:8002`  
- **Notification Service** → background Kafka worker  

### User Service

```bash
cd user-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001
````

### Order Service

```bash
cd order-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

### Notification Service (Worker)

```bash
cd notification-service
pip install -r requirements.txt
python3 -m app.worker
```

## Nginx Reverse Proxy Setup

We use **Nginx** to expose all services under a single domain.

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 2. Create Config File

```bash
sudo nano /etc/nginx/sites-available/food-delivery-api.conf
```

```nginx
server {
    listen 80;
    server_name food.delivery.my;

    location /health {
        return 200 "OK";
        add_header Content-Type text/plain;
    }

    location /v1/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /v1/orders/ {
        proxy_pass http://127.0.0.1:8002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Enable & Reload

```bash
sudo ln -sf /etc/nginx/sites-available/food-delivery-api.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx reload
```

## API Documentation

* User Service → `http://food.delivery.my/v1/docs`
* Order Service → `http://food.delivery.my/v1/orders/docs`
* Health check → `http://food.delivery.my/health`
