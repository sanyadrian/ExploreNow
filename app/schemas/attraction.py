from pydantic import BaseModel

class AttractionSchema(BaseModel):
    type: str = "attraction"
    name: str | None
    address: str | None
    rating: float | None
    lat: float | None
    lng: float | None
    distance_km: float | None = None
    source: str = "google"
