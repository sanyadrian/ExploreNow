from pydantic import BaseModel
from typing import Optional

class EventSchema(BaseModel):
    type: str = "event"
    name: Optional[str]
    date: Optional[str]
    time: Optional[str]
    venue: Optional[str]
    city: Optional[str]
    url: Optional[str]
    venue_latitude: Optional[float] = None
    venue_longitude: Optional[float] = None
    distance_km: Optional[float] = None
    source: str = "ticketmaster"
