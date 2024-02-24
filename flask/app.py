# System
from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Security dependencies 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

# Other dependencies
import os
import json

# Sources
STORES_JSON_PATH = '../data/test.json'

# Env setting
env_file = '.env.production' if os.getenv('FLASK_ENV') == 'production' else '.env.local'
load_dotenv(env_file)
DATACENTER_API_BASE_URL = os.getenv('DATACENTER_API_BASE_URL')


app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})


app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# User data
users = {
    "jerry": generate_password_hash("0000")
}

# 🐞 Debug URL
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API"}), 200

# Account
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
@app.route('/save_json', methods=['POST'])
def save_json():
    # Make a backup of the current stores.json, if it exists
    if os.path.exists('stores.json'):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        os.rename('stores.json', f'stores_backup_{timestamp}.json')

    # Save the new JSON data
    data = request.json
    with open('stores.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify({"message": "JSON data saved successfully"}), 200


@app.route('/stores', methods=['GET'])
def get_stores():
    if os.path.exists(STORES_JSON_PATH):
        with open(STORES_JSON_PATH, 'r', encoding='utf-8') as file:
            stores_data = json.load(file)
        return jsonify(stores_data)
    else:
        return jsonify({"error": "stores.json not found"}), 404

@app.route('/stores', methods=['POST'])
@jwt_required()  # Assuming you want to protect this endpoint
def save_stores():
    # Make a backup of the current stores.json, if it exists
    if os.path.exists(STORES_JSON_PATH):
        backup_path = STORES_JSON_PATH.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
        os.rename(STORES_JSON_PATH, backup_path)

    # Save the new JSON data
    data = request.json
    with open(STORES_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return jsonify({"message": "stores.json updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
