import httpx
from app.core.config import settings

class EventbriteService:
    BASE_URL = "https://www.eventbriteapi.com/v3/events/search/"

    def __init__(self):
        self.api_key = settings.eventbrite_api_key

    async def get_events_by_city(
        self,
        city: str,
        keyword: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        page: int = 1
    ):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        params = {
            "location.address": city,
            "expand": "venue",
            "page": page
        }

        if keyword:
            params["q"] = keyword
        if start_date:
            params["start_date.range_start"] = start_date
        if end_date:
            params["start_date.range_end"] = end_date

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, headers=headers, params=params)
            print("Final URL:", response.url)
            print("Status:", response.status_code)
            print("Response Text:", response.text)
            response.raise_for_status()
            data = response.json()

        results = []
        for event in data.get("events", []):
            venue = event.get("venue", {})
            address = venue.get("address", {})

            results.append({
                "name": event.get("name", {}).get("text"),
                "start_time": event.get("start", {}).get("local"),
                "venue": venue.get("name"),
                "city": address.get("city"),
                "url": event.get("url"),
            })

        return results
