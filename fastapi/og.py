from flask import Blueprint, request, render_template, current_app, send_from_directory
import requests

# Data path
STORES_JSON_PATH = 'https://www.deejiar.com/stores.json'
app_directory = '/var/www/deejiar'

# Blueprint for Open Graph functionalities
og_bp = Blueprint('og', __name__, template_folder='templates')

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
@og_bp.route('/detail/<path:title>')
def detail(title):
    current_app.logger.debug('Headers: %s', request.headers)
    user_agent = request.headers.get('User-Agent', '').lower()
    bots = ['facebookexternalhit', 'twitterbot', 'linkedinbot']
    if any(bot in user_agent for bot in bots):
        image_url = get_meta_image_url_from_title(title)
        description = 'Map for Taste Adventurers to Explore without Boundaries'
        return render_template('bot_response.html', image_url=image_url, title="Deejiar", description=description)
    # If the request does NOT come from the bots, pass to CSR by Vue
    else:
        return send_from_directory(app_directory, 'index.html')