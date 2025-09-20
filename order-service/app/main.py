from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routes.order_routes import OrderRoutes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", root_path="/v1/orders")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

order_routes = OrderRoutes()
app.include_router(order_routes.router)
