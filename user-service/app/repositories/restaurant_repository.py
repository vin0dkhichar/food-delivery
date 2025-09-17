from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant


class RestaurantRepository:
    def create_restaurant(self, db: Session, restaurant: Restaurant) -> Restaurant:
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        return restaurant

    def get_restaurant_by_id(self, db: Session, restaurant_id: int):
        return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def get_all_restaurants(self, db: Session):
        return db.query(Restaurant).all()
