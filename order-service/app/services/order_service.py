# app/services/order_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order_schema import OrderCreate
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, db: Session, user_id: int, order_data: OrderCreate) -> Order:
        new_order = Order(user_id=user_id, restaurant_id=order_data.restaurant_id)
        db.add(new_order)
        db.flush()

        for item in order_data.items:
            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price=item.price,
            )
            new_order.items.append(order_item)

        db.commit()
        db.refresh(new_order)
        return new_order

    def get_order(self, db: Session, user_id: int, order_id: int) -> Optional[Order]:
        order = self.repository.get_order(db, order_id)
        if not order or order.user_id != user_id:
            return None
        return order

    def list_orders(self, db: Session, user_id: int) -> List[Order]:
        return self.repository.list_orders_by_user(db, user_id)

    def update_order_status(
        self, db: Session, order_id: int, status: OrderStatus
    ) -> Optional[Order]:
        order = self.repository.get_order(db, order_id)
        if not order:
            return None
        order.status = status
        db.commit()
        db.refresh(order)
        return order
