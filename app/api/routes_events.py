from fastapi import APIRouter, Query
from app.services.eventbrite import EventbriteService

router = APIRouter()
eventbrite_service = EventbriteService()

@router.get("/eventbrite")
async def get_eventbrite_events(city: str = Query(...), keyword: str | None = None):
    data = await eventbrite_service.get_events_by_city(city, keyword)
    return {"results": data}
