from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.menu_item_schema import MenuItemCreate
from app.core.search import index_document


class MenuItemService:
    def __init__(self, db: Session):
        self.db = db

    def create_menu_item(self, data: MenuItemCreate, current_user: User) -> MenuItem:
        restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.id == data.restaurant_id)
            .first()
        )
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
            )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to add menu items to this restaurant",
            )

        menu_item = MenuItem(
            name=data.name,
            description=data.description,
            price=data.price,
            is_available=data.is_available,
            category=data.category,
            cuisine_type=data.cuisine_type,
            tags=data.tags or [],
            restaurant_id=data.restaurant_id,
            image_id=data.image_id if data.image_id else None,
        )
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)

        index_document(
            index="menu_items",
            id=menu_item.id,
            body={
                "name": menu_item.name,
                "description": menu_item.description,
                "price": menu_item.price,
                "is_available": menu_item.is_available,
                "category": menu_item.category,
                "cuisine_type": menu_item.cuisine_type,
                "tags": menu_item.tags,
                "restaurant_id": menu_item.restaurant_id,
            },
        )
        return menu_item

    def get_menu_item_by_id(self, item_id: int):
        return self.db.query(MenuItem).filter(MenuItem.id == item_id).first()

    def get_menu_items_by_restaurant(self, restaurant_id: int):
        return (
            self.db.query(MenuItem)
            .filter(MenuItem.restaurant_id == restaurant_id)
            .all()
        )
