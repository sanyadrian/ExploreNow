import math

def haversine(lat1, lng1, lat2, lng2):
    R = 6371  # Earth radius in KM
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlng/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

CATEGORY_MAP = {
    # Ticketmaster categories
    "concerts": {"tm_keyword": "concert"},
    "sports": {"tm_keyword": "sports"},
    "theatre": {"tm_keyword": "theatre"},
    "festivals": {"tm_keyword": "festival", "google_keyword": "festival"},

    # Google categories
    "museums": {"google_type": "museum"},
    "parks": {"google_type": "park"},
    "nightlife": {"google_keyword": "nightlife"},
    "attractions": {"google_type": "tourist_attraction"},
}

