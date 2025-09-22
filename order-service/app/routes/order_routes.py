from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.core.kafka_producer import send_order_created_event
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.core.logger import logger


class OrderRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/orders", tags=["Orders"])
        self.order_service = OrderService(OrderRepository())

        self.router.add_api_route(
            "/",
            self.create_order,
            response_model=OrderResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/",
            self.list_orders,
            response_model=list[OrderResponse],
            methods=["GET"],
        )

        self.router.add_api_route(
            "/{order_id}",
            self.get_order,
            response_model=OrderResponse,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/{order_id}/status",
            self.update_order_status,
            response_model=OrderResponse,
            methods=["PUT"],
        )

    def create_order(
        self,
        order_data: OrderCreate,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        logger.info("Received request to create order for user_id=%s", current_user.id)

        order = self.order_service.create_order(db, current_user.id, order_data)

        subject = f"Order Confirmation - #{order.id}"
        message = (
            f"Hello {current_user.full_name},\n\n"
            f"Thank you for your order! Your order with ID #{order.id} has been successfully created.\n"
            f"We will notify you once it's on the way.\n\n"
            f"Order Details:\n"
            f"- Order ID: {order.id}\n"
            f"- Status: {order.status}\n\n"
            f"Thank you for shopping with us!\n"
            f"Best regards,\n"
            f"The Eat Tree Team"
        )

        self._send_order_email(current_user, order, subject, message)

        logger.info("Order created successfully: order_id=%s", order.id)
        return order

    def get_order(
        self,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        logger.info(
            "Request to fetch order_id=%s for user_id=%s", order_id, current_user.id
        )

        order = self.order_service.get_order(db, current_user.id, order_id)

        if not order:
            logger.warning("Order not found: order_id=%s", order_id)
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def list_orders(
        self,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        logger.info("Request to list orders for user_id=%s", current_user.id)
        return self.order_service.list_orders(db, current_user.id)

    def update_order_status(
        self,
        order_id: int,
        status_data: OrderStatusUpdate,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        logger.info(
            "Request to update order_id=%s to status=%s",
            order_id,
            status_data.status.value,
        )

        order = self.order_service.update_order_status(db, order_id, status_data.status)

        if not order:
            logger.warning("Order not found for status update: order_id=%s", order_id)
            raise HTTPException(status_code=404, detail="Order not found")

        subject = f"Order Update - #{order.id}"

        message = (
            f"Hello {current_user.full_name},\n\n"
            f"Your order with ID #{order.id} status has been updated to **{status_data.status.value.upper()}**.\n\n"
            f"Thank you for shopping with us!\n"
            f"Best regards,\n"
            f"The Eat Tree Team"
        )

        logger.debug("Sending order status update event for order_id=%s", order.id)

        self._send_order_email(current_user, order, subject, message)

        logger.info("Order status updated and notification sent: order_id=%s", order.id)
        return order

    def _send_order_email(self, user: TokenData, order, subject: str, message: str):
        """Common method to send order-related emails via Kafka event"""
        logger.debug("Producing Kafka event for order_id=%s", order.id)

        send_order_created_event(
            {
                "user_id": user.id,
                "name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "order_id": order.id,
                "subject": subject,
                "message": message,
            }
        )
