from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant_schema import RestaurantCreate
from app.repositories.restaurant_repository import RestaurantRepository


class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def create_restaurant(
        self, db: Session, owner_id: int, data: RestaurantCreate
    ) -> Restaurant:
        new_restaurant = Restaurant(
            name=data.name,
            description=data.description,
            address=data.address,
            phone_number=data.phone_number,
            owner_id=owner_id,
            is_active=True,
        )
        return self.repository.create_restaurant(db, new_restaurant)

    def get_restaurant_by_id(self, db: Session, restaurant_id: int) -> Restaurant:
        return self.repository.get_restaurant_by_id(db, restaurant_id)

    def get_all_restaurants(self, db: Session):
        return self.repository.get_all_restaurants(db)
