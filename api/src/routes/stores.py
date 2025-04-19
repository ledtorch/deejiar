from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Store, StoreMetadata
from database import get_db

router = APIRouter()

@router.get("/store/{store_id}")
def get_store_metadata(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    metadata = db.query(StoreMetadata).filter(StoreMetadata.store_id == store_id).first()
    
    if not store:
        return {"error": "Store not found"}
    
    return {
        "id": store.id,
        "name": store.name,
        "coordinates": {"lat": store.lat, "lng": store.lng},
        "metadata": metadata
    }