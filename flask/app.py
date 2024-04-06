# System
from flask import Flask, request, jsonify

# Security and authentication 
from werkzeug.security import check_password_hash, generate_password_hash

from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Environment
from dotenv import load_dotenv

# Data
import os
import json
from datetime import datetime, timedelta

# OG image feature
from og import og_bp
from werkzeug.middleware.proxy_fix import ProxyFix

# Debug
import logging

# Env setting
env_file = '.env.production' if os.getenv('FLASK_ENV') == 'production' else '.env.local'
load_dotenv(env_file)

# Files and sources
STORES_JSON_PATH = '../data/stores.json'
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

# JSON
@app.route('/stores', methods=['POST'])
def update_json():
    # Make a backup of the current stores.json
    if os.path.exists(STORES_JSON_PATH):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_path = STORES_JSON_PATH.replace('.json', f'_backup_{timestamp}.json')
        os.rename(STORES_JSON_PATH, backup_path)

    # Save the new JSON data
    data = request.json
    with open(STORES_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify({"message": "JSON data updated successfully"}), 200

@app.route('/stores', methods=['GET'])
def get_stores():
    if os.path.exists(STORES_JSON_PATH):
        with open(STORES_JSON_PATH, 'r', encoding='utf-8') as file:
            stores_data = json.load(file)
        return jsonify(stores_data)
    else:
        return jsonify({"error": "stores.json not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
