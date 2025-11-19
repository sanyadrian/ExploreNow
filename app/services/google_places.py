import httpx
from app.core.config import settings


class GooglePlacesService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    def __init__(self):
        self.api_key = settings.google_api_key

    async def get_places_by_location(self, lat:float, lng:float, radius: int = 2000, type_: str = "tourist_attraction", keyword: str | None = None):
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": type_,
            "key": self.api_key
        }
        if keyword:
            params["keyword"] = keyword

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        results = []
        for place in data.get("results", []):
            location = place.get("geometry", {}).get("location", {})
            results.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating"),
                "user_rating_total": place.get("user_rating_total"),
                "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                "lng": place.get("geometry", {}).get("location", {}).get("lng")
            })
        return results


