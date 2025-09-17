from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.restaurant_schema import RestaurantCreate, RestaurantResponse
from app.services.restaurant_service import RestaurantService
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/restaurants", tags=["restaurants"])
restaurant_service = RestaurantService(RestaurantRepository())


@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "restaurant":
        raise HTTPException(status_code=403, detail="Only restaurant owners can create")

    return restaurant_service.create_restaurant(db, current_user.id, data)


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    restaurant = restaurant_service.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/", response_model=list[RestaurantResponse])
def list_all_restaurants(db: Session = Depends(get_db)):
    return restaurant_service.get_all_restaurants(db)
