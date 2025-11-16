from pydantic import BaseModel
from typing import Optional

class EventSchema(BaseModel):
    name: Optional[str]
    date: Optional[str]
    time: Optional[str]
    venue: Optional[str]
    city: Optional[str]
    url: Optional[str]
    distance_km: Optional[float] = None   # for /nearby sorting
