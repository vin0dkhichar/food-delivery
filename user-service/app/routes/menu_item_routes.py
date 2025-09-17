from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.menu_item_schema import MenuItemCreate, MenuItemResponse
from app.services.menu_item_service import MenuItemService
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/menu-items", tags=["menu-items"])
menu_item_service = MenuItemService(MenuItemRepository(), RestaurantRepository())


@router.post("/{restaurant_id}", response_model=MenuItemResponse)
def create_menu_item(
    restaurant_id: int,
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    created = menu_item_service.create_menu_item(
        db, restaurant_id, current_user.id, data
    )
    if created is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if created is False:
        raise HTTPException(status_code=403, detail="Not authorized to add items")
    return created


@router.get("/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = menu_item_service.get_menu_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.get("/restaurant/{restaurant_id}", response_model=list[MenuItemResponse])
def list_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    return menu_item_service.get_menu_items_by_restaurant(db, restaurant_id)
