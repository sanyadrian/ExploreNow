from fastapi import APIRouter, Query
from app.services.ticketmaster import TicketmasterService
from app.core.utils import haversine

router = APIRouter()
ticketmaster_service = TicketmasterService()


@router.get("/")
async def get_all_events(
    lat: float = Query(...),
    lng: float = Query(...),
    keyword: str | None = None,
    radius: int = 25
):

    data = await ticketmaster_service.get_events(
        lat=lat,
        lng=lng,
        keyword=keyword,
        radius=radius
    )
    return {"results": data}


@router.get("/ticketmaster")
async def get_ticketmaster_events(
    lat: float | None = None,
    lng: float | None = None,
    city: str | None = None,
    keyword: str | None = None,
    radius: int = 25
):
    data = await ticketmaster_service.get_events(
        lat=lat,
        lng=lng,
        city=city,
        keyword=keyword,
        radius=radius
    )
    return {"results": data}

@router.get("/sorted")
async def get_ticketmaster_events_sorted(
        lat: float | None = None,
        lng: float | None = None,
        keyword: str | None = None,
):
    data = await ticketmaster_service.get_events(
        lat=lat, lng=lng, keyword=keyword
    )

    sorted_events = sorted(data, key=lambda event: (event.date or "9999-99-99", event.time or "99:99:99"))
    return {"results": sorted_events}


@router.get("/nearby")
async def get_nearby_events(
    lat: float = Query(...),
    lng: float = Query(...),
    keyword: str | None = None
):
    events = await ticketmaster_service.get_events(lat=lat, lng=lng, keyword=keyword)

    for e in events:
        if e.city:
            venue_data = e.__dict__
            venue_lat = venue_data.get("latitude")
            venue_lng = venue_data.get("longitude")

            if venue_lat and venue_lng:
                e.distance_km = haversine(lat, lng, venue_lat, venue_lng)

    sorted_events = sorted(events, key=lambda x: x.distance_km or 999999)

    return {"results": sorted_events}