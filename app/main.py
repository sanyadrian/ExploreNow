from fastapi import FastAPI
from app.api import routes_places, routes_events

app = FastAPI(title="ExploreNow API", version="1.0")

app.include_router(routes_places.router, prefix="/places", tags=["Places"])
app.include_router(routes_events.router, prefix="/events", tags=["Events"])

@app.get("/")
def root():
    return {"message": "Starting"}
