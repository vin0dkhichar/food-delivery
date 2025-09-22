from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item_schema import MenuItemCreate
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.logger import logger


class MenuItemService:
    def __init__(
        self, repository: MenuItemRepository, restaurant_repo: RestaurantRepository
    ):
        self.repository = repository
        self.restaurant_repo = restaurant_repo

    def create_menu_item(
        self, db: Session, restaurant_id: int, owner_id: int, data: MenuItemCreate
    ) -> MenuItem:
        logger.info("Start create_menu_item for restaurant_id=%s", restaurant_id)

        restaurant = self.restaurant_repo.get_restaurant_by_id(db, restaurant_id)

        if not restaurant:
            logger.error("Restaurant not found: id=%s", restaurant_id)
            return None

        if restaurant.owner_id != owner_id:
            logger.error(
                "Unauthorized attempt by user_id=%s for restaurant_id=%s",
                owner_id,
                restaurant_id,
            )
            return False

        new_item = MenuItem(
            name=data.name,
            description=data.description,
            price=data.price,
            is_available=data.is_available,
            restaurant_id=restaurant_id,
        )

        created_item = self.repository.create_menu_item(db, new_item)

        logger.info("Menu item created with id=%s", created_item.id)
        return created_item

    def get_menu_item_by_id(self, db: Session, item_id: int):
        return self.repository.get_menu_item_by_id(db, item_id)

    def get_menu_items_by_restaurant(self, db: Session, restaurant_id: int):
        return self.repository.get_menu_items_by_restaurant(db, restaurant_id)
