from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant_schema import RestaurantCreate
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.logger import logger


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
            is_active=True,
        )

        created_restaurant = self.repository.create_restaurant(db, new_restaurant)

        logger.info("Restaurant created with id=%s", created_restaurant.id)
        return created_restaurant

    def get_restaurant_by_id(self, db: Session, restaurant_id: int) -> Restaurant:
        return self.repository.get_restaurant_by_id(db, restaurant_id)

    def get_all_restaurants(self, db: Session):
        return self.repository.get_all_restaurants(db)
