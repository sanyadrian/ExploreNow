from fastapi import APIRouter, Query
from app.services.ticketmaster import TicketmasterService

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
