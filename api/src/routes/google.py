import os
import json
import requests
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from fastapi import HTTPException

# Adjust sys.path to include the parent directory (src)
sys.path.append(str(Path(__file__).resolve().parent.parent))

# ─── Load Environment ─────────────────────────────
load_dotenv('../../.env.local')  # Adjust path as needed
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_NEWPLACE_API_KEY', 'APIKEY')

# ─── Fetch Nearby Places (New Places API) ─────────
def fetch_places_from_google_v1(
    lat: float,
    lng: float,
    radius: int = 1000,
    place_type: str = "restaurant",
    max_results: int = 20
) -> dict:
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.types"
    }
    body = {
        "includedTypes": [place_type],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": radius
            }
        }
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Google Places API (v1): {str(e)}")

# ─── Fetch Place Details (optional use) ───────────
def get_place_details(place_id: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,geometry,photos,opening_hours,types,rating,user_ratings_total,price_level",
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching place details: {str(e)}")

# ─── Main Runner ──────────────────────────────────
if __name__ == "__main__":
    try:
        # Set search target
        lat = 25.0330
        lng = 121.5654
        place_type = "restaurant"
        radius = 1000

        print(f"🔍 Fetching {place_type}s near {lat},{lng}...")
        places = fetch_places_from_google_v1(lat, lng, radius, place_type)
        count = len(places.get("places", []))
        print(f"✅ Fetched {count} places.")

        # Pretty print (optional)
        print(json.dumps(places, indent=2, ensure_ascii=False))

        # Save result to /data
        output_dir = Path("../../data")  # Adjust if needed
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / "google_places_20.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(places, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved raw API response to: {filename}")

        # Convert to Deejiar format
        from google_data_converter import convert_to_deejiar_format, save_filtered_places
        google_places = places.get("places", [])
        layout = "food"  # Change as needed
        converted = convert_to_deejiar_format(google_places, place_type, layout)

        # Save converted data using the converter's save function
        converted_filename = save_filtered_places(f"deejiar_{place_type}", converted)
        print(f"✨ Saved converted Deejiar data to: /data/{converted_filename}")

    except Exception as e:
        print(f"🚨 Error: {str(e)}")