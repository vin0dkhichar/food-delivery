from sqlalchemy.orm import Session
from app.models.menu_item import MenuItem
from app.schemas.menu_item_schema import MenuItemCreate
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository


class MenuItemService:
    def __init__(
        self, repository: MenuItemRepository, restaurant_repo: RestaurantRepository
    ):
        self.repository = repository
        self.restaurant_repo = restaurant_repo

    def create_menu_item(
        self, db: Session, restaurant_id: int, owner_id: int, data: MenuItemCreate
    ) -> MenuItem:
        restaurant = self.restaurant_repo.get_restaurant_by_id(db, restaurant_id)
        if not restaurant:
            return None
        if restaurant.owner_id != owner_id:
            return False

        new_item = MenuItem(
            name=data.name,
            description=data.description,
            price=data.price,
            is_available=data.is_available,
            restaurant_id=restaurant_id,
        )
        return self.repository.create_menu_item(db, new_item)

    def get_menu_item_by_id(self, db: Session, item_id: int):
        return self.repository.get_menu_item_by_id(db, item_id)

    def get_menu_items_by_restaurant(self, db: Session, restaurant_id: int):
        return self.repository.get_menu_items_by_restaurant(db, restaurant_id)
