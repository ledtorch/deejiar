from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pathlib import Path
import json

router = APIRouter()

# Cache for meta data to improve performance
_meta_cache: Optional[Dict[str, Any]] = None


async def load_meta_data() -> Dict[str, Any]:
    """
    Load and cache meta.json data for search operations.
    Returns cached data if available, otherwise loads from file.
    """
    global _meta_cache
    
    if _meta_cache is None:
        # Navigate to assets/map directory
        base_path = Path(__file__).resolve().parent.parent.parent / "assets" / "map"
        meta_path = base_path / "meta.json"
        
        if not meta_path.exists():
            raise HTTPException(
                status_code=500, 
                detail="Search data file not found"
            )
        
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                _meta_cache = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Invalid search data format"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load search data: {str(e)}"
            )
    
    return _meta_cache


def calculate_relevance_score(query: str, title: str) -> float:
    """
    Calculate relevance score for search results ranking.
    Higher scores indicate better matches.
    """
    query_lower = query.lower()
    title_lower = title.lower()
    
    if title_lower == query_lower:
        return 2.0  # Exact match
    elif title_lower.startswith(query_lower):
        return 1.5  # Starts with query
    elif query_lower in title_lower:
        # Partial match - score based on position
        position = title_lower.index(query_lower)
        return 1.0 - (position * 0.01)  # Earlier matches score higher
    return 0.0


def filter_by_type(features: List[Dict], store_type: str) -> List[Dict]:
    """Filter features by store type."""
    type_lower = store_type.lower()
    return [
        feature for feature in features
        if feature.get("properties", {}).get("type", "").lower() == type_lower
    ]


def filter_by_tags(features: List[Dict], tags: List[str]) -> List[Dict]:
    """Filter features by store tags (OR operation - any tag matches)."""
    if not tags:
        return features
    
    tags_lower = [tag.lower() for tag in tags]
    filtered = []
    
    for feature in features:
        store_tags = feature.get("properties", {}).get("storetag", [])
        store_tags_lower = [tag.lower() for tag in store_tags]
        
        # Check if any requested tag is in store tags
        if any(tag in store_tags_lower for tag in tags_lower):
            filtered.append(feature)
    
    return filtered


@router.get("")
async def search_stores(
    q: Optional[str] = Query(None, description="Search query for store names"),
    type: Optional[str] = Query(None, description="Filter by store type (e.g., cafe, bar, restaurant)"),
    tags: Optional[List[str]] = Query(None, description="Filter by store tags (e.g., cashonly, takeaway)"),
    limit: Optional[int] = Query(50, description="Maximum number of results to return", ge=1, le=100)
) -> Dict[str, Any]:
    """
    Search stores by name with optional type and tag filters.
    
    Returns:
        GeoJSON features matching the search criteria with relevance scoring.
    
    Examples:
        - /api/search?q=cafe
        - /api/search?type=bar
        - /api/search?q=tea&type=cafe
        - /api/search?tags=cashonly&tags=takeaway
    """
    
    # Load search data
    try:
        meta_data = await load_meta_data()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search service error: {str(e)}"
        )
    
    # Validate data structure
    if not meta_data or "features" not in meta_data:
        raise HTTPException(
            status_code=500,
            detail="Invalid search data structure"
        )
    
    features = meta_data["features"]
    results = []
    
    # Step 1: Text search (if query provided)
    if q:
        query_lower = q.lower().strip()
        
        for feature in features:
            properties = feature.get("properties", {})
            title = properties.get("title", "")
            
            # Calculate relevance score
            score = calculate_relevance_score(q, title)
            
            if score > 0:
                results.append((score, feature))
        
        # Sort by relevance score (highest first)
        results.sort(key=lambda x: x[0], reverse=True)
        results = [feature for _, feature in results]
    else:
        # No query - start with all features
        results = features.copy()
    
    # Step 2: Apply type filter
    if type:
        results = filter_by_type(results, type)
    
    # Step 3: Apply tag filters
    if tags:
        results = filter_by_tags(results, tags)
    
    # Step 4: Apply limit
    results = results[:limit]
    
    # Return response
    return {
        "results": results,
        "count": len(results),
        "total": len(features),
        "query": q,
        "filters": {
            "type": type,
            "tags": tags,
            "limit": limit
        }
    }


@router.get("/types")
async def get_store_types() -> Dict[str, Any]:
    """
    Get all available store types for filtering.
    Useful for populating filter dropdowns in the UI.
    """
    meta_data = await load_meta_data()
    features = meta_data.get("features", [])
    
    # Collect unique types
    types = set()
    for feature in features:
        store_type = feature.get("properties", {}).get("type")
        if store_type:
            types.add(store_type)
    
    # Sort and structure response
    sorted_types = sorted(types)
    
    return {
        "types": sorted_types,
        "count": len(sorted_types)
    }


@router.get("/tags")
async def get_store_tags() -> Dict[str, Any]:
    """
    Get all available store tags for filtering.
    Useful for populating filter options in the UI.
    """
    meta_data = await load_meta_data()
    features = meta_data.get("features", [])
    
    # Collect unique tags
    tags = set()
    for feature in features:
        store_tags = feature.get("properties", {}).get("storetag", [])
        for tag in store_tags:
            if tag:
                tags.add(tag)
    
    # Sort and structure response
    sorted_tags = sorted(tags)
    
    return {
        "tags": sorted_tags,
        "count": len(sorted_tags)
    }


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="Partial query for suggestions", min_length=1)
) -> Dict[str, Any]:
    """
    Get search suggestions based on partial input.
    Returns up to 10 matching store names for autocomplete.
    """
    meta_data = await load_meta_data()
    features = meta_data.get("features", [])
    
    query_lower = q.lower().strip()
    suggestions = []
    
    for feature in features:
        title = feature.get("properties", {}).get("title", "")
        title_lower = title.lower()
        
        # Check if title contains or starts with query
        if query_lower in title_lower:
            score = 2.0 if title_lower.startswith(query_lower) else 1.0
            suggestions.append((score, title))
    
    # Sort by relevance and limit to 10
    suggestions.sort(key=lambda x: x[0], reverse=True)
    suggestions = [title for _, title in suggestions][:10]
    
    return {
        "suggestions": suggestions,
        "count": len(suggestions),
        "query": q
    }


# Optional: Clear cache function (useful for development)
async def clear_search_cache():
    """Clear the cached meta data. Useful when data is updated."""
    global _meta_cache
    _meta_cache = None
    return {"message": "Search cache cleared"}