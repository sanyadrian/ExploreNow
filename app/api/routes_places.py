from fastapi import APIRouter, Query

from app.services.google_places import GooglePlacesService

router = APIRouter()
places_service = GooglePlacesService()

@router.get("/")
async def get_places(lat: float = Query(...), lng: float = Query(...), radius: int = 2000):
    data = await places_service.get_places_by_location(lat, lng, radius)
    return {"results": data}
