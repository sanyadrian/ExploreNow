from fastapi import APIRouter, Query
from app.services.ticketmaster import TicketmasterService
from app.services.google_places import GooglePlacesService
from app.core.utils import haversine
from app.core.utils import CATEGORY_MAP

router = APIRouter()
ticketmaster_service = TicketmasterService()
google_places_service = GooglePlacesService()


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
    lat: float = Query(...),
    lng: float = Query(...),
    keyword: str | None = None
):
    events = await ticketmaster_service.get_events(
        lat=lat,
        lng=lng,
        keyword=keyword
    )

    sorted_events = sorted(
        events,
        key=lambda e: (
            e.date or "9999-99-99",
            e.time or "99:99:99"
        )
    )

    return {"results": [event.model_dump() for event in sorted_events]}


@router.get("/nearby")
async def get_nearby_events(
    lat: float = Query(...),
    lng: float = Query(...),
    keyword: str | None = None
):
    events = await ticketmaster_service.get_events(lat=lat, lng=lng, keyword=keyword)

    for e in events:
        if e.venue_latitude and e.venue_longitude:
            e.distance_km = haversine(lat, lng, e.venue_latitude, e.venue_longitude)

    sorted_events = sorted(events, key=lambda x: x.distance_km or 999999)

    return {"results": [e.model_dump() for e in sorted_events]}


@router.get("/explore")
async def explore(
        lat: float = Query(...),
        lng: float = Query(...),
        keyword: str | None = None,
        category: str | None = None,
        sort_by: str = "distance"
):

    google_type = "tourist_attraction"
    google_keyword = keyword
    tm_keyword = keyword

    if category and category.lower() in CATEGORY_MAP:
        cfg = CATEGORY_MAP[category.lower()]

        if "google_type" in cfg:
            google_type = cfg["google_type"]

        if "google_keyword" in cfg:
            google_keyword = cfg["google_keyword"]

        if "tm_keyword" in cfg:
            tm_keyword = cfg["tm_keyword"]


    attractions = await google_places_service.get_places_by_location(
        lat=lat,
        lng=lng,
        radius=2000,
        type_=google_type,
        keyword=google_keyword,
    )
    google_only_categories = {"museums", "parks", "nightlife", "attractions"}
    if category and category.lower() in google_only_categories:
        events = []
    else:
        events = await ticketmaster_service.get_events(
            lat=lat,
            lng=lng,
            keyword=tm_keyword
        )

    combined = []

    for place in attractions:
        combined.append({
            "type": "attraction",
            "name": place["name"],
            "address": place["address"],
            "rating": place["rating"],
            "distance_km": haversine(lat, lng, place["lat"], place["lng"]),
            "source": "google",
        })

    for ev in events:
        if ev.venue_latitude and ev.venue_longitude:
            distance = haversine(lat, lng, ev.venue_latitude, ev.venue_longitude)
        else:
            distance = None

        combined.append({
            "type": "event",
            "name": ev.name,
            "date": ev.date,
            "time": ev.time,
            "venue": ev.venue,
            "city": ev.city,
            "url": ev.url,
            "distance_km": distance,
            "source": "ticketmaster",
        })

    if sort_by == "distance":
        combined = sorted(combined, key=lambda x: x["distance_km"] or 99999)

    if sort_by == "popularity":
        combined = sorted(combined, key=lambda x: x.get("rating", 0), reverse=True)

    return {"results": combined}