from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import requests
import os

# Data path
STORES_JSON_PATH = 'https://www.deejiar.com/stores.json'
app_directory = '/var/www/deejiar'

# Router for Open Graph functionalities
og_router = APIRouter()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Generate meta content for image
def get_meta_image_url_from_title(title):
    response = requests.get(STORES_JSON_PATH)
    if response.status_code == 200:
        stores_data = response.json()
        for store in stores_data['features']:
            if store['properties']['title'] == title:
                image_path = store['properties'].get('item1', {}).get('image', '')
                image_url = f'https://www.deejiar.com/{image_path}'
                return image_url
    # Return default image
    return 'https://www.deejiar.com/images/og-image.jpg'

# Generate meta template
@og_router.get("/detail/{title}", response_class=HTMLResponse)
async def detail(title: str, request: Request):
    user_agent = request.headers.get('User-Agent', '').lower()
    bots = ['facebookexternalhit', 'twitterbot', 'linkedinbot']
    if any(bot in user_agent for bot in bots):
        image_url = get_meta_image_url_from_title(title)
        description = 'Map for Taste Adventurers to Explore without Boundaries'
        return templates.TemplateResponse("bot_response.html", {"request": request, "image_url": image_url, "title": "Deejiar", "description": description})
    # If the request does NOT come from the bots, pass to CSR by Vue
    else:
        index_path = os.path.join(app_directory, 'index.html')
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail="Index file not found")