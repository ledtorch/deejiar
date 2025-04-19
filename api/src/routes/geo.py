from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/geo/stores")
def get_stores():
    with open("data/stores.json") as f:
        stores_data = json.load(f)
    return stores_data