import httpx
from app.core.config import settings


class GooglePlacesService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    def __init__(self):
        self.api_key = settings.google_api_key

    async def get_places_by_location(self, lat:float, lng:float, radius: int = 2000, type_: str = "tourist_attraction"):
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": type_,
            "key": self.api_key
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        results = []
        for place in data.get(results, []):
            results.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating"),
                "user_rating_total": place.get("user_rating_total"),
            })
        return results


