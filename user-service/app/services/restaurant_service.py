from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant_schema import RestaurantCreate
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.logger import logger
from app.core.search import index_document


class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def create_restaurant(
        self, db: Session, owner_id: int, data: RestaurantCreate
    ) -> Restaurant:
        logger.info("Start create_restaurant for owner_id=%s", owner_id)

        new_restaurant = Restaurant(
            name=data.name,
            description=data.description,
            address=data.address,
            phone_number=data.phone_number,
            owner_id=owner_id,
            category=data.category,
            cuisine_type=data.cuisine_type,
            tags=data.tags or [],
            latitude=data.latitude,
            longitude=data.longitude,
            is_active=True,
        )

        created_restaurant = self.repository.create_restaurant(db, new_restaurant)

        index_document(
            index="restaurants",
            id=created_restaurant.id,
            body={
                "name": created_restaurant.name,
                "description": created_restaurant.description,
                "address": created_restaurant.address,
                "category": created_restaurant.category,
                "cuisine_type": created_restaurant.cuisine_type,
                "tags": created_restaurant.tags,
                "location": {
                    "lat": created_restaurant.latitude,
                    "lon": created_restaurant.longitude,
                },
            },
        )

        logger.info("Restaurant created with id=%s", created_restaurant.id)
        return created_restaurant

    def get_restaurant_by_id(self, db: Session, restaurant_id: int) -> Restaurant:
        return self.repository.get_restaurant_by_id(db, restaurant_id)

    def get_all_restaurants(self, db: Session):
        return self.repository.get_all_restaurants(db)
