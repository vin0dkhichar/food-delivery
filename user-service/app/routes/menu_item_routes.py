from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.menu_item_schema import MenuItemCreate, MenuItemResponse
from app.services.menu_item_service import MenuItemService
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.dependencies import get_current_user
from app.models.user import User


class MenuItemRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/menu-items", tags=["Menu Items"])
        self.menu_item_service = MenuItemService(
            MenuItemRepository(), RestaurantRepository()
        )

        self.router.add_api_route(
            "/{restaurant_id}",
            self.create_menu_item,
            response_model=MenuItemResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/{item_id}",
            self.get_menu_item,
            response_model=MenuItemResponse,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/restaurant/{restaurant_id}",
            self.list_menu_items,
            response_model=list[MenuItemResponse],
            methods=["GET"],
        )

    def create_menu_item(
        self,
        restaurant_id: int,
        data: MenuItemCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        created = self.menu_item_service.create_menu_item(
            db, restaurant_id, current_user.id, data
        )
        if created is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
            )
        if created is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to add items",
            )
        return created

    def get_menu_item(
        self,
        item_id: int,
        db: Session = Depends(get_db),
    ):
        item = self.menu_item_service.get_menu_item_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
            )
        return item

    def list_menu_items(
        self,
        restaurant_id: int,
        db: Session = Depends(get_db),
    ):
        return self.menu_item_service.get_menu_items_by_restaurant(db, restaurant_id)
