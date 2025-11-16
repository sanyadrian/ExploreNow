import httpx
from app.core.config import settings

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
        radius: int = 25,  # in miles
        start_date: str | None = None,
        end_date: str | None = None,
        size: int = 20,
    ):
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
            print("Final URL:", response.url)
            response.raise_for_status()
            data = response.json()

        results = []
        for event in data.get("_embedded", {}).get("events", []):
            venue_info = event.get("_embedded", {}).get("venues", [{}])[0]
            city_name = venue_info.get("city", {}).get("name")
            results.append({
                "name": event.get("name"),
                "date": event.get("dates", {}).get("start", {}).get("localDate"),
                "time": event.get("dates", {}).get("start", {}).get("localTime"),
                "venue": venue_info.get("name"),
                "city": city_name,
                "url": event.get("url"),
            })

        return results
