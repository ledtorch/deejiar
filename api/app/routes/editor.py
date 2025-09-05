import os
import json
from fastapi import HTTPException, UploadFile, File
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Load environment variables
from dotenv import load_dotenv
load_dotenv('../.env.local')

# Define JSON_PATH relative to this file
JSON_PATH = Path(__file__).parent.parent.parent / 'assets/map'
print(f"JSON_PATH: {JSON_PATH}")

def list_json_files() -> List[str]:
    """List all JSON files in the map directory"""
    try:
        # Ensure directory exists
        if not JSON_PATH.exists():
            JSON_PATH.mkdir(parents=True, exist_ok=True)
            return []
        
        # List all files in the directory
        files = os.listdir(JSON_PATH)
        
        # Filter out files to only include .json files
        json_files = [file for file in files if file.endswith('.json')]
        print(f"json_files: {json_files}")
        return json_files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

def get_json_data(filename: str) -> Dict[str, Any]:
    """Get the raw JSON data from a file"""
    # Remove .json extension if present
    if filename.endswith('.json'):
        filename = filename[:-5]
    
    path = JSON_PATH / f"{filename}.json"
    
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}.json")
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

def save_json_data(filename: str, data: Dict[str, Any]) -> str:
    """Save JSON data directly without reconstruction"""
    try:
        # Remove .json extension if present
        if filename.endswith('.json'):
            filename = filename[:-5]
        
        # Generate timestamp
        timestamp = datetime.utcnow().strftime("_%m%dT%H%M%S")
        
        # Handle existing timestamps in filename
        base_name = filename
        if '_' in filename:
            parts = filename.rsplit('_', 1)
            # Check if the last part looks like a timestamp (11 characters: MMDDTHHMMSS)
            if len(parts) == 2 and len(parts[1]) == 11 and parts[1][4] == 'T':
                base_name = parts[0]
        
        # Create new filename with timestamp
        new_filename = f"{base_name}{timestamp}.json"
        
        # Save the JSON to a file
        full_path = JSON_PATH / new_filename
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved file: {new_filename}")
        return new_filename
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")