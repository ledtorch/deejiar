# Standard libraries
import os
import json
from datetime import datetime, timedelta

# Environment settings
from dotenv import load_dotenv

# Flask framework
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

# Security and utilities
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

# Local modules
from og import og_bp
import reader

# Env setting
env_file = '.env.production' if os.getenv('FLASK_ENV') == 'production' else '.env.local'
load_dotenv(env_file)

# Files and sources
# STORES_JSON_PATH = '../data/stores.json'
STORES_JSON_PATH = '../data/'
DATACENTER_API_BASE_URL = os.getenv('DATACENTER_API_BASE_URL')

# User account
users = {
    "jerry": generate_password_hash("0000")
}

# Flask app config
app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})
# Auth
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Register the blueprint for OG image feature
app.register_blueprint(og_bp)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# 🐞 Debug URL, check deejiar.com/admin/api
@app.route('/')
def home():
    print("Home route accessed")
    return jsonify({"message": "Flask Server"}), 200

# Account
# 🏗️ expires seems doesn't match the real timeframe
@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    username = credentials.get('account')
    password = credentials.get('password')
    # expires = timedelta(minutes=30)
    expires = timedelta(seconds=5)

    if username in users and check_password_hash(users[username], password):
        access_token = create_access_token(identity=username, expires_delta=expires)
        return jsonify({"message": "Login successful", "access_token": access_token, "redirect": "/dashboard"}), 200    
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Dashboard
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# 🧱 Working
@app.route('/json-files', methods=['GET'])
def get_json_files():
    json_files = reader.list_json_files()
    return jsonify(json_files)

@app.route('/json-data/<filename>', methods=['GET'])
def get_json_data(filename):
    simplified_data = reader.flatten_features(f'{filename}.json')
    if simplified_data is not None:
        return jsonify(simplified_data)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/save/<filename>', methods=['POST'])
def update_json(filename):
    base_directory = '../data/'
    json_file_path = os.path.join(base_directory, f"{filename}.json")

    # Make a backup of the current JSON file
    if os.path.exists(json_file_path):
        timestamp = datetime.now().strftime('%H%M%S')
        backup_path = json_file_path.replace('.json', f'_backup_{timestamp}.json')
        os.rename(json_file_path, backup_path)
    else:
        # If the file does not exist, do not proceed
        return jsonify({"error": "File not found"}), 404

    # Get the edited data from the request
    edited_data = request.json

    try:
        # Use the reconstruct_json function to rebuild the JSON structure
        reconstructed_data = reader.reconstruct_json(edited_data)

        # Save the new JSON data
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(reconstructed_data, f, ensure_ascii=False, indent=4)

    except ValueError as e:
        # Handle the error by returning an error response
        return jsonify({"error": str(e)}), 400  # Bad request due to data error

    # If everything went well
    return jsonify({"message": f"{filename} updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
