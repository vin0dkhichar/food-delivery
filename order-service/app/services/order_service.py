from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order_schema import OrderCreate
from app.repositories.order_repository import OrderRepository
from app.core.logger import logger


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, db: Session, user_id: int, order_data: OrderCreate) -> Order:
        logger.info("Creating a new order for user_id=%s", user_id)

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

            logger.debug(
                "Added item %s (quantity=%s, price=%s) to order_id=%s",
                item.menu_item_id,
                item.quantity,
                item.price,
                new_order.id,
            )

        db.commit()
        db.refresh(new_order)

        logger.info("Order created successfully: order_id=%s", new_order.id)
        return new_order

    def get_order(self, db: Session, user_id: int, order_id: int) -> Optional[Order]:
        logger.info("Fetching order_id=%s for user_id=%s", order_id, user_id)

        order = self.repository.get_order(db, order_id)

        if not order or order.user_id != user_id:
            logger.warning("Order not found: order_id=%s", order_id)
            return None
        return order

    def list_orders(self, db: Session, user_id: int) -> List[Order]:
        logger.info("Listing orders for user_id=%s", user_id)

        orders = self.repository.list_orders_by_user(db, user_id)

        logger.debug("Found %d orders for user_id=%s", len(orders), user_id)
        return orders

    def update_order_status(
        self, db: Session, order_id: int, status: OrderStatus
    ) -> Optional[Order]:
        logger.info("Updating order_id=%s to status=%s", order_id, status.value)

        order = self.repository.get_order(db, order_id)

        if not order:
            logger.warning("Order not found for update: order_id=%s", order_id)
            return None

        old_status = order.status
        order.status = status
        db.commit()
        db.refresh(order)

        logger.info(
            "Order status updated: order_id=%s from %s to %s",
            order_id,
            old_status.value,
            status.value,
        )
        return order
