from pydantic import BaseModel
from typing import Union
from app.schemas.event import EventSchema
from app.schemas.attraction import AttractionSchema

class ExploreItem(BaseModel):
    item: Union[EventSchema, AttractionSchema]
