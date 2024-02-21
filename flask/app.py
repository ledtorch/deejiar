from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# Security dependencies 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Editing JSON dependencies
import os
import json
from datetime import datetime

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
jwt = JWTManager(app)

# Example user data
users = {
    "jerry": generate_password_hash("0000")
}

# Account
@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    username = credentials.get('account')
    password = credentials.get('password')

    if username in users and check_password_hash(users[username], password):
        access_token = create_access_token(identity=username)
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

if __name__ == '__main__':
    app.run(debug=True)
