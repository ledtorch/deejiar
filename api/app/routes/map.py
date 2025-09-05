from fastapi import APIRouter
import os
import json
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi import HTTPException

router = APIRouter()

@router.get("/map/{filename}")
def get_map_json(filename: str):
    # Ensure only .json files are allowed
    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported.")

    base_path = Path(__file__).resolve().parent.parent.parent / "assets" / "map"
    file_path = base_path / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON file.")