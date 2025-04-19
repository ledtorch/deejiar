from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)  # Unique store ID
    name = Column(String, nullable=False)
    google_place_id = Column(String, unique=True, nullable=True)  # Optional Google Place ID
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    metadata = relationship("StoreMetadata", back_populates="store", uselist=False)


class StoreMetadata(Base):
    __tablename__ = "store_metadata"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=True)
    images = Column(JSON)  # Storefront images
    description = Column(String)
    tags = Column(JSON)  # List of tags like ["wifi", "pet-friendly"]
    business_hours = Column(JSON)  # JSON object for open-close times
    menu = Column(JSON)  # Store menu items

    store = relationship("Store", back_populates="metadata")