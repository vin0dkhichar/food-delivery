from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.order import Order


class OrderRepository:
    def create_order(self, db: Session, order: Order) -> Order:
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    def get_order(self, db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()

    def list_orders_by_user(self, db: Session, user_id: int) -> List[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()
