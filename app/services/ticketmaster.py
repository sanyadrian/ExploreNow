import httpx
import json
from app.core.config import settings
from app.schemas.event import EventSchema
from app.core.cache import redis_client


class TicketmasterService:
    BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

    def __init__(self):
        self.api_key = settings.ticketmaster_api_key

    async def get_events(
        self,
        lat: float | None = None,
        lng: float | None = None,
        city: str | None = None,
        keyword: str | None = None,
        radius: int = 25,
        start_date: str | None = None,
        end_date: str | None = None,
        size: int = 20,
    ):
        cache_key = f"tm:{lat}:{lng}:{city}:{keyword}:{radius}:{start_date}:{end_date}:{size}"
        cached = await redis_client.get(cache_key)

        if cached:
            return [EventSchema(**item) for item in json.loads(cached)]

        params = {
            "apikey": self.api_key,
            "size": size,
            "radius": radius,
            "sort": "date,asc"
        }

        if lat and lng:
            params["latlong"] = f"{lat},{lng}"
        elif city:
            params["city"] = city

        if keyword:
            params["keyword"] = keyword
        if start_date:
            params["startDateTime"] = start_date
        if end_date:
            params["endDateTime"] = end_date

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            data = response.json()

        results = []
        for event in data.get("_embedded", {}).get("events", []):
            venue_info = event.get("_embedded", {}).get("venues", [{}])[0]
            location_info = venue_info.get("location", {})
            venue_lat = float(location_info.get("latitude")) if location_info.get("latitude") else None
            venue_lng = float(location_info.get("longitude")) if location_info.get("longitude") else Non
            city_name = venue_info.get("city", {}).get("name")

            results.append(EventSchema(
                name=event.get("name"),
                date=event.get("dates", {}).get("start", {}).get("localDate"),
                time=event.get("dates", {}).get("start", {}).get("localTime"),
                venue=venue_info.get("name"),
                city=city_name,
                url=event.get("url"),
                venue_latitude = venue_lat,
                venue_longitude = venue_lng
            ))

        await redis_client.setex(
            cache_key,
            600,
            json.dumps([e.model_dump() for e in results])
        )

        return results
