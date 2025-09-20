from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem


class MenuItemRepository:
    def create_menu_item(self, db: Session, menu_item: MenuItem) -> MenuItem:
        db.add(menu_item)
        db.commit()
        db.refresh(menu_item)
        return menu_item

    def get_menu_item_by_id(self, db: Session, item_id: int):
        return db.query(MenuItem).filter(MenuItem.id == item_id).first()

    def get_menu_items_by_restaurant(self, db: Session, restaurant_id: int):
        return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
