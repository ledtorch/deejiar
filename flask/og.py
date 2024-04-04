from flask import Blueprint, request, render_template, current_app, send_from_directory
import requests
import json

# Blueprint for Open Graph functionalities
og_bp = Blueprint('og', __name__, template_folder='templates')

STORES_JSON_PATH = 'https://www.deejiar.com/stores.json'

app_directory = '/var/www/deejiar'

def get_image_url_for_title(title):
    response = requests.get(STORES_JSON_PATH)
    if response.status_code == 200:
        stores_data = response.json()
        for store in stores_data['features']:
            if store['properties']['title'] == title:
                image_path = store['properties'].get('item1', {}).get('image', '')
                # Check if image_path already includes the domain
                if not image_path.startswith('http'):
                    # If not, prepend the domain to the image_path
                    image_url = f'https://www.deejiar.com/{image_path}'
                else:
                    image_url = image_path
                return image_url
    return ''  # Return an empty string if not found or request failed

@og_bp.route('/detail/<path:title>')
def detail(title):
    current_app.logger.debug('Headers: %s', request.headers)
    user_agent = request.headers.get('User-Agent', '').lower()
    bots = ['facebookexternalhit', 'twitterbot', 'linkedinbot']
    if any(bot in user_agent for bot in bots):
        image_url = get_image_url_for_title(title)
        return render_template('bot_response.html', image_url=image_url, title="Deejiar", description="The App.")
    else:
        return send_from_directory(app_directory, 'index.html')





