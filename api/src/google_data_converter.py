import os
import json
import requests
from fastapi import HTTPException
from pathlib import Path
from datetime import datetime
import uuid
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env.local')

# Define JSON_PATH relative to this file
JSON_PATH = Path(__file__).parent.parent / 'data'

# Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def fetch_places_from_google(
    query: str, 
    location: str, 
    radius: int = 5000, 
    place_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch places from Google Maps API based on search criteria
    
    Args:
        query: Search term (e.g., "coffee shops")
        location: Latitude,longitude (e.g., "37.7749,-122.4194" for San Francisco)
        radius: Search radius in meters
        place_type: Optional place type (e.g., "restaurant", "cafe")
    
    Returns:
        Dictionary containing the Google Places API response
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    if place_type:
        params["type"] = place_type
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Google Maps API: {str(e)}")

def get_place_details(place_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a place using its place_id
    
    Args:
        place_id: Google Maps place ID
    
    Returns:
        Dictionary containing the place details
    """
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,geometry,photos,opening_hours,types,rating,user_ratings_total,price_level",
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching place details: {str(e)}")

def convert_to_deejiar_format(google_places: List[Dict[str, Any]], place_type: str, layout: str) -> Dict[str, Any]:
    """
    Convert Google Places data to Deejiar JSON format matching the single-feature.json example.
    """
    features = []
    for i, place in enumerate(google_places):
        # Try geometry.location (old format), else location (current format)
        location = place.get("geometry", {}).get("location")
        if not location:
            location = place.get("location", {})
        lng = location.get("lng") or location.get("longitude")
        lat = location.get("lat") or location.get("latitude")
        if lng is None or lat is None:
            continue
        # Compose feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]
            },
            "properties": {
                "title": place.get("name") or place.get("displayName", {}).get("text", ""),
                "type": place_type,
                "address": place.get("formatted_address", ""),
                "auid": str(uuid.uuid4()),
                "placeid": place.get("place_id") or place.get("id", ""),
                "businesshour": extract_business_hours(place),
                "description": place.get("vicinity", "") or place.get("formatted_address", ""),
                "icon": {
                    "active": f"button/marker/{place_type}-active.png",
                    "default": f"button/marker/{place_type}-default.png",
                    "larger": f"button/marker/{place_type}-larger.png",
                    "mini": f"button/marker/{place_type}-mini.png",
                    "withFriends": f"button/marker/{place_type}-withFriends.png"
                },
                "id": str(i + 1),
                "item1": {"name": "", "description": "", "image": "", "price": ""},
                "item2": {"name": "", "description": "", "image": "", "price": ""},
                "item3": {"name": "", "description": "", "image": "", "price": ""},
                "item4": {"name": "", "description": "", "image": "", "price": ""},
                "item5": {"name": "", "description": "", "image": "", "price": ""},
                "layout": layout,
                "storefront": {"day": "", "night": ""},
                "tag": str(extract_tags_from_place(place))
            }
        }
        features.append(feature)
    return {
        "type": "FeatureCollection",
        "features": features
    }

def extract_tags_from_place(place: Dict[str, Any]) -> List[str]:
    """
    Extract relevant tags from a Google Place
    
    Args:
        place: Google Place data
    
    Returns:
        List of tags
    """
    tags = []
    
    # Extract from types
    types = place.get("types", [])
    
    # Map Google types to Deejiar tags
    type_to_tag = {
        "restaurant": "food",
        "cafe": "coffee",
        "bar": "drinks",
        "bakery": "bakery",
        "book_store": "books",
        "clothing_store": "fashion",
        "shopping_mall": "shopping",
        "museum": "culture",
        "art_gallery": "art",
        "park": "outdoor",
        "library": "books",
        "gym": "fitness",
        "spa": "wellness"
    }
    
    for type_name in types:
        if type_name in type_to_tag:
            tags.append(type_to_tag[type_name])
    
    # Add price level tag if available
    price_level = place.get("price_level")
    if price_level is not None:
        price_tag = "$" * (price_level + 1)
        tags.append(price_tag)
    
    # Add rating-based tag
    rating = place.get("rating")
    if rating is not None:
        if rating >= 4.5:
            tags.append("top-rated")
        elif rating >= 4.0:
            tags.append("highly-rated")
    
    return tags

def extract_business_hours(place: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract business hours from a Google Place
    
    Args:
        place: Google Place data
    
    Returns:
        List of business hour objects in Deejiar format
    """
    business_hours = [
        {
            "24hr": False,
            "Holiday": []
        }
    ]
    
    # Days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Get opening hours from place details
    opening_hours = place.get("opening_hours", {})
    periods = opening_hours.get("periods", [])
    
    # If no periods, mark all days as closed
    if not periods:
        for day in days:
            business_hours.append({day: False})
        return business_hours
    
    # Process each day
    for day_index, day in enumerate(days):
        day_periods = []
        
        # Find periods for this day
        for period in periods:
            open_day = period.get("open", {}).get("day")
            close_day = period.get("close", {}).get("day")
            
            if open_day == day_index:
                open_time = period.get("open", {}).get("time", "0000")
                close_time = period.get("close", {}).get("time", "0000")
                
                day_periods.append({
                    "Start": open_time,
                    "Finish": close_time
                })
        
        # If no periods for this day, mark as closed
        if not day_periods:
            business_hours.append({day: False})
        else:
            business_hours.append({day: day_periods})
    
    return business_hours

def save_filtered_places(filename: str, data: Dict[str, Any]) -> str:
    """
    Save filtered places data to a JSON file
    
    Args:
        filename: Base filename (without extension)
        data: Data to save
    
    Returns:
        Name of the saved file
    """
    # Add .json extension if it's missing
    if not filename.lower().endswith('.json'):
        filename += '.json'
    
    timestamp = datetime.utcnow().strftime("_%m%dT%H:%M:%S")
    
    # Check if filename already has a timestamp and replace it, or add a new one
    base_name, extension = os.path.splitext(filename)
    if '_' in base_name:
        parts = base_name.rsplit('_', 1)
        # 13 is the length of "MMDDTHH:MM:SS"
        if len(parts) == 2 and len(parts[1]) == 13:
            new_filename = f"{parts[0]}{timestamp}{extension}"
        else:
            new_filename = f"{base_name}{timestamp}{extension}"
    else:
        new_filename = f"{base_name}{timestamp}{extension}"
    
    # Save the JSON to a file
    full_path = os.path.join(JSON_PATH, new_filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return new_filename