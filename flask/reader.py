import os
import json

# Files and sources
JSON_PATH = '../data'

def list_json_files():
    # List all files in the directory
    files = os.listdir(JSON_PATH)
    # Filter out files to only include .json files
    json_files = [file for file in files if file.endswith('.json')]
    return json_files

# Extract features as single layer objects in an array
def flatten_features(filename):
    path = os.path.join(JSON_PATH, filename)
    if not os.path.exists(path):
        return None

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        simplified_data = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            icon = props.get('icon', {}).get('active', '').split('/')[-1].replace('-active.png', '')
            simplified_data.append({
                # basicProperties
                'id': props.get('id'),
                'title': props.get('title'),
                'type': props.get('type'),
                'layout': props.get('layout'),
                'description': props.get('description'),
                'icon': icon,
                'storefront': storefront,
                # geoProperties
                'address': props.get('address'),
                'auid': props.get('auid'),
                'placeid': props.get('placeid'),
                'longitude': geometry.get('coordinates', [])[0],
                'latitude': geometry.get('coordinates', [])[1],
                # productProperties
                # timeProperties
            })
    return simplified_data

# Rebuild the nested JSON structure from the flattened data
def reconstruct_json(features):
    reconstructed = {
        "type": "FeatureCollection",
        "features": []
    }
    for feature in features:
        # If an icon is missing, stopping the entire process
        icon = feature.get('icon')
        if not icon:
            raise ValueError(f"Missing icon name for feature ID: {feature.get('id')}")
        
        reconstructed_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                # geoProperties
                "coordinates": [feature.get('longitude'), feature.get('latitude')]
            },
            "properties": {
                # basicProperties
                "id": feature.get('id'),
                "title": feature.get('title'),
                "type": feature.get('type'),
                "layout": feature.get('layout'),
                "description": feature.get('description'),
                "icon": {
                    "active": f"button/marker/{icon}-active.png",
                    "default": f"button/marker/{icon}-default.png",
                    "larger": f"button/marker/{icon}-larger.png",
                    "mini": f"button/marker/{icon}-mini.png",
                    "withFriends": f"button/marker/{icon}-withFriends.png"
                },

                # geoProperties
                "address": feature.get('address'),
                "auid": feature.get('auid'),
                "placeid": feature.get('placeid'),
                
                # productProperties
                
                # timeProperties
            }
        }
        reconstructed['features'].append(reconstructed_feature)
    return reconstructed

