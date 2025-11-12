from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_places():
    return {"message": "Places"}