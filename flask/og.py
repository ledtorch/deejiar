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





{"creation_number":0,"account_address":"04dbae908dfc2f904386f3f1181f4db0c43b402ae77bc72881d210e531cbf1b1"},"sequence_number":0,"type_tag":{"struct":{"address":"0000000000000000000000000000000000000000000000000000000000000001","module":"account","name":"CoinRegisterEvent","type_args":[]}},"event_data":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,10,97,112,116,111,115,95,99,111,105,110,9,65,112,116,111,115,67,111,105,110]}},{"V2":{"type_tag":{"struct":{"address":"0000000000000000000000000000000000000000000000000000000000000001","module":"transaction_fee","name":"FeeStatement","type_args":[]}},"event_data":[225,3,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,240,129,1,0,0,0,0,0,0,0,0,0,0,0,0,0]}}],"confirmation_time":1712229027534804,"block_number":232,"block_hash":"816ebf2779c7e09b79f751e6b77c754af50b407ae7640371784e9fc9f89a092f","status":"Success"}