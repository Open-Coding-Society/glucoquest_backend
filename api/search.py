import os
import sys
import json
import logging

# Dynamically add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from flask import Flask, request, jsonify, Blueprint, g
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from model.search import SearchHistory, db
from api.jwt_authorize import token_required
from model.user import User

# Initialize Flask app
app = Flask(__name__)

# Apply CORS settings to the app
CORS(app, supports_credentials=True, resources={
    "/api/*": {
        "origins": "http://127.0.0.1:4887",  # Exact origin of your frontend
        "methods": ["GET", "POST", "OPTIONS"],  # Allowed HTTP methods
        "allow_headers": ["Content-Type", "Authorization"],  # Allowed headers
    }
})

# Define the Blueprint
search_api = Blueprint("search_api", __name__, url_prefix="/api/search")

# Items data
items = [
       {"name": "Teddy Bear", "link": "/holiday_frontend/holiday/toys", "tags": {"all": 1, "teddy": 0, "bear": 0, "toys": 0}},
       {"name": "Lego Set", "link": "/holiday_frontend/holiday/toys", "tags": {"all": 1, "lego": 0, "set": 0, "toys": 0}},
       {"name": "Remote Control Car", "link": "/holiday_frontend/holiday/toys", "tags": {"all": 1, "remote": 0, "control": 0, "car": 0, "toys": 0}},
       {"name": "Holiday Candles", "link": "/holiday_frontend/holiday/home-decor", "tags": {"all": 1, "holiday": 0, "candles": 0, "home-decor": 0}},
       {"name": "Festive Wreath", "link": "/holiday_frontend/holiday/home-decor", "tags": {"all": 1, "festive": 0, "wreath": 0, "home-decor": 0}},
       {"name": "Decorative Ornaments", "link": "/holiday_frontend/holiday/home-decor", "tags": {"all": 1, "decorative": 0, "ornaments": 0, "home-decor": 0}},
       {"name": "Wireless Headphones", "link": "/holiday_frontend/holiday/electronics", "tags": {"all": 1, "wireless": 0, "headphones": 0, "electronics": 0}},
       {"name": "Smartwatch", "link": "/holiday_frontend/holiday/electronics", "tags": {"all": 1, "smartwatch": 0, "electronics": 0}},
       {"name": "Gaming Console", "link": "/holiday_frontend/holiday/electronics", "tags": {"all": 1, "gaming": 0, "console": 0, "electronics": 0}},
       {"name": "Cozy Holiday Sweater", "link": "/holiday_frontend/holiday/clothes", "tags": {"all": 1, "cozy": 0, "holiday": 0, "sweater": 0, "clothes": 0}},
       {"name": "Woolen Scarf", "link": "/holiday_frontend/holiday/clothes", "tags": {"all": 1, "woolen": 0, "scarf": 0, "clothes": 0}},
       {"name": "Winter Gloves", "link": "/holiday_frontend/holiday/clothes", "tags": {"all": 1, "winter": 0, "gloves": 0, "clothes": 0}},
       {"name": "Holiday Cookies", "link": "/holiday_frontend/holiday/food", "tags": {"all": 1, "holiday": 0, "cookies": 0, "food": 0}},
       {"name": "Chocolate Gift Box", "link": "/holiday_frontend/holiday/food", "tags": {"all": 1, "chocolate": 0, "gift": 0, "box": 0, "food": 0}},
       {"name": "Gourmet Cheese Set", "link": "/holiday_frontend/holiday/food", "tags": {"all": 1, "gourmet": 0, "cheese": 0, "set": 0, "food": 0}},
       {"name": "Scented Candle", "link": "/holiday_frontend/holiday/scented", "tags": {"all": 1, "candle": 0, "scented": 0}},
       {"name": "Aromatic Diffuser", "link": "/holiday_frontend/holiday/scented", "tags": {"all": 1, "aromatic": 0, "diffuser": 0, "scented": 0}},
       {"name": "Perfume Gift Set", "link": "/holiday_frontend/holiday/scented", "tags": {"all": 1, "perfume": 0, "gift": 0, "set": 0, "scented": 0}}
]

# Path to JSON file for backups
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "../searchHistory.json")

# Helper function to append data to the JSON file
def append_to_json(data):
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r") as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = []

        # Append the new data
        existing_data.append(data)

        # Write back to the file
        with open(JSON_FILE_PATH, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")

#PUT FUNCTION
@search_api.route("/update", methods=["PUT"])
@token_required()
def update_search_history():
    """
    Updates a specific entry in the search_history table based on the provided ID.
    """
    data = request.get_json()  # Parse the JSON body
    if not data or "id" not in data:
        return jsonify({"error": "Invalid request. ID is required."}), 400

    search_id = data["id"]  # ID of the item to update

    # Find the existing entry in the database
    search_entry = SearchHistory.query.filter_by(id=search_id).first()
    if not search_entry:
        return jsonify({"error": "Item not found."}), 404

    # Update fields if provided
    if "name" in data:
        search_entry.name = data["name"]

    if "tags" in data:
        search_entry.tags = data["tags"]

    # Save changes to the database
    try:
        db.session.commit()
        return jsonify({"message": "Item updated successfully!", "item": search_entry.read()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update item: {str(e)}"}), 500

#GET FUNCTION
@search_api.route("", methods=["GET"])
@token_required()
def search_items():
    """
    Search for items based on a query string.
    """
    query = request.args.get("q", "").lower()
    current_user = g.current_user  # Get authenticated user
    user_id = current_user.uid

    if not query:
        return jsonify([])

    # Match items based on whether the query is in the name (case-insensitive, partial match)
    results = [
        {"name": item["name"], "link": item["link"], "tags": item["tags"]}
        for item in items if query in item["name"].lower()
    ]

    return jsonify(results), 200

#POST FUNCTION
@search_api.route("/increment_tag", methods=["POST"])
@token_required()
def increment_tag():
    """
    Increment the tags for a specific item for the authenticated user.
    Save the user's selection in the database and also to the JSON file.
    """
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid data"}), 400

    current_user = g.current_user  # Get authenticated user
    item_name = data["name"]

    # Find the item in the catalog by name
    item = next((item for item in items if item["name"].lower() == item_name.lower()), None)
    if item:
        # Increment tags for the item
        for tag in item["tags"]:
            item["tags"][tag] += 1

        # Save the user's selection (item name, tags) in the database
        try:
            search_entry = SearchHistory(
                user=current_user.uid,
                name=item["name"],  # Exact item name from dictionary
                tags=item["tags"],  # Tags of the item
                query=None  # No query saved
            )
            db.session.add(search_entry)
            db.session.commit()

            # Save to JSON file
            append_to_json(search_entry.read())
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to log item selection: {str(e)}"}), 500

        return jsonify({
            "message": f"Tags for '{item_name}' updated successfully!",
            "tags": item["tags"]
        }), 200

    return jsonify({"error": "Item not found!"}), 404


# Ensure CORS headers are added to all responses
@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:4887"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# Register the Blueprint
app.register_blueprint(search_api)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8209)

# Testy stuff for sqllite database
# ./scripts/db_init.py 
# ./scripts/db_backup.py
# ./scripts/db_restore.py