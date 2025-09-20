from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.core.kafka_producer import send_order_created_event
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository


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

    def create_order(
        self,
        order_data: OrderCreate,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        order = self.order_service.create_order(db, current_user.id, order_data)

        send_order_created_event(
            {
                "user_id": current_user.id,
                "email": current_user.email,
                "phone_number": current_user.phone_number,
                "order_id": order.id,
                "message": f"Your order {order.id} has been created!",
            }
        )
        return order

    def get_order(
        self,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        order = self.order_service.get_order(db, current_user.id, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def list_orders(
        self,
        db: Session = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
    ):
        return self.order_service.list_orders(db, current_user.id)
