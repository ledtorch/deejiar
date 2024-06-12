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
            storefront = props.get('storefront', {})
            feature_dict = ({
                # basicProperties
                'id': props.get('id'),
                'title': props.get('title'),
                'type': props.get('type'),
                'layout': props.get('layout'),
                'icon': icon,
                'description': props.get('description'),
                'storefront-day': storefront.get('day', ''),
                'storefront-night': storefront.get('night', ''),
                
                # geoProperties
                'address': props.get('address'),
                'auid': props.get('auid'),
                'placeid': props.get('placeid'),
                'longitude': geometry.get('coordinates', [])[0],
                'latitude': geometry.get('coordinates', [])[1],
                
                # Tags
                'tag': props.get('tag', []),

                # Business Hours
                'businesshour': props.get('businesshour', [])
            })
            # productProperties
            for i in range(1, 6):
                feature_dict[f'item{i}'] = props.get(f'item{i}', {})

            simplified_data.append(feature_dict)
            # timeProperties
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
                "icon": {
                    "active": f"button/marker/{icon}-active.png",
                    "default": f"button/marker/{icon}-default.png",
                    "larger": f"button/marker/{icon}-larger.png",
                    "mini": f"button/marker/{icon}-mini.png",
                    "withFriends": f"button/marker/{icon}-withFriends.png"
                },
                "description": feature.get('description'),
                "storefront": {
                    "day": feature.get('storefront-day'),
                    "night": feature.get('storefront-night')
                },
                
                # geoProperties
                "address": feature.get('address'),
                "auid": feature.get('auid'),
                "placeid": feature.get('placeid'),

                # Tags
                'tag': feature.get('tag', []),

                # Business Hours
                'businesshour': feature.get('businesshour', [])
            }
        }
        # productProperties
        for i in range(1, 6):
            reconstructed_feature['properties'][f'item{i}'] = feature.get(f'item{i}', {})

        reconstructed['features'].append(reconstructed_feature)
        # timeProperties
    return reconstructed

