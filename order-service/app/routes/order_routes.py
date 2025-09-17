from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService(OrderRepository())


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    return order_service.create_order(db, current_user.id, order_data)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    order = order_service.get_order(db, current_user.id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    return order_service.list_orders(db, current_user.id)
