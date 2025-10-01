from fastapi import APIRouter, Query
from app.core.search import search_documents

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/restaurants")
def search_restaurants(q: str = Query(...)):
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": [
                    "name^3",
                    "description",
                    "address",
                    "category",
                    "cuisine_type",
                    "tags",
                ],
            }
        }
    }
    results = search_documents("restaurants", query)
    return results["hits"]["hits"]


@router.get("/menu-items")
def search_menu_items(q: str = Query(...)):
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["name^3", "description", "category", "cuisine_type", "tags"],
            }
        }
    }
    results = search_documents("menu_items", query)
    return results["hits"]["hits"]


@router.get("/restaurants/nearby")
def search_restaurants_nearby(lat: float, lon: float, distance: str = "5km"):
    query = {
        "query": {
            "bool": {
                "filter": {
                    "geo_distance": {
                        "distance": distance,
                        "location": {"lat": lat, "lon": lon},
                    }
                }
            }
        },
        "sort": [
            {
                "_geo_distance": {
                    "location": {"lat": lat, "lon": lon},
                    "order": "asc",
                    "unit": "km",
                }
            }
        ],
    }
    results = search_documents("restaurants", query)
    return results["hits"]["hits"]
