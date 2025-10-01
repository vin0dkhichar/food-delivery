from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.menu_item_schema import MenuItemResponse, MenuItemCreate
from app.services.menu_item_service import MenuItemService
from app.core.dependencies import get_current_user
from app.models.user import User


class MenuItemRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/menu-items", tags=["Menu Items"])
        self.router.add_api_route(
            "/",
            self.create_menu_item,
            methods=["POST"],
            response_model=MenuItemResponse,
            status_code=201,
        )
        self.router.add_api_route(
            "/{item_id}",
            self.get_menu_item,
            methods=["GET"],
            response_model=MenuItemResponse,
        )
        self.router.add_api_route(
            "/restaurant/{restaurant_id}",
            self.list_menu_items,
            methods=["GET"],
            response_model=List[MenuItemResponse],
        )

    def create_menu_item(
        self,
        data: MenuItemCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = MenuItemService(db)
        menu_item = service.create_menu_item(data, current_user)
        return MenuItemResponse.from_orm(menu_item)

    def get_menu_item(self, item_id: int, db: Session = Depends(get_db)):
        service = MenuItemService(db)
        item = service.get_menu_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return MenuItemResponse.from_orm(item)

    def list_menu_items(self, restaurant_id: int, db: Session = Depends(get_db)):
        service = MenuItemService(db)
        items = service.get_menu_items_by_restaurant(restaurant_id)
        return [MenuItemResponse.from_orm(item) for item in items]
