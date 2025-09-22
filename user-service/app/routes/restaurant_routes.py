from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.restaurant_schema import RestaurantCreate, RestaurantResponse
from app.services.restaurant_service import RestaurantService
from app.repositories.restaurant_repository import RestaurantRepository
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.logger import logger


class RestaurantRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
        self.restaurant_service = RestaurantService(RestaurantRepository())

        self.router.add_api_route(
            "/",
            self.create_restaurant,
            response_model=RestaurantResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/{restaurant_id}",
            self.get_restaurant,
            response_model=RestaurantResponse,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/",
            self.list_all_restaurants,
            response_model=list[RestaurantResponse],
            methods=["GET"],
        )

    def create_restaurant(
        self,
        data: RestaurantCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        logger.info("Start create_restaurant by user_id=%s", current_user.id)

        if current_user.role != "restaurant":
            logger.error(
                "Unauthorized restaurant create attempt user_id=%s", current_user.id
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can create",
            )

        restaurant = self.restaurant_service.create_restaurant(
            db, current_user.id, data
        )

        logger.info("Restaurant created id=%s", restaurant.id)
        return restaurant

    def get_restaurant(
        self,
        restaurant_id: int,
        db: Session = Depends(get_db),
    ):
        logger.info("Start get_restaurant id=%s", restaurant_id)
        restaurant = self.restaurant_service.get_restaurant_by_id(db, restaurant_id)
        if not restaurant:
            logger.error("Restaurant not found id=%s", restaurant_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
            )

        logger.info("Returning restaurant id=%s", restaurant_id)
        return restaurant

    def list_all_restaurants(self, db: Session = Depends(get_db)):
        return self.restaurant_service.get_all_restaurants(db)
