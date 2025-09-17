from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import order_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

app.include_router(order_routes.router)
