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
            simplified_data.append({
                'id': props.get('id'),
                'title': props.get('title'),
                'type': props.get('type'),
                'layout': props.get('layout'),
                'address': props.get('address'),
                'auid': props.get('auid'),
                'placeid': props.get('placeid'),
                'longitude': geometry.get('coordinates', [])[0],
                'latitude': geometry.get('coordinates', [])[1]
            })
    return simplified_data
