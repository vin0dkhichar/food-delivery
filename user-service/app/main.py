from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user_routes, restaurant_routes, menu_item_routes
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", root_path="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(restaurant_routes.router)
app.include_router(menu_item_routes.router)
