from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from flask_restful import Api, Resource
from flask import Blueprint

# Initialize Flask app
app = Flask(__name__)

# Add max entries limit to prevent memory issues
MAX_WISHLIST_ENTRIES = 100

# Update CORS configuration
CORS(app,
     supports_credentials=True,
     origins=['http://localhost:4000', 'http://localhost:3000', 'http://0.0.0.0:4000', 'http://127.0.0.1:4000'],
     methods=['GET', 'POST', 'DELETE'],
     allow_headers=['Content-Type'])

wishlist_api = Blueprint('wishlist_api', __name__, url_prefix='/api')
# Simulated database for wishlists
wishlist_db = {}

@app.route('/api/wishlist', methods=['GET'])
def get_wishlist():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        wishlist = wishlist_db.get(user_id, [])
        return jsonify({"wishlist": wishlist}), 200
    except Exception as e:
        app.logger.error(f"Error in get_wishlist: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/wishlist', methods=['POST'])
def add_to_wishlist():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_id = data.get('user_id')
        item = data.get('item')

        if not user_id or not item:
            return jsonify({"error": "user_id and item are required"}), 400

        if user_id not in wishlist_db:
            wishlist_db[user_id] = []

        if len(wishlist_db[user_id]) >= MAX_WISHLIST_ENTRIES:
            return jsonify({"error": "Wishlist is full"}), 400

        wishlist_db[user_id].append(item)
        return jsonify({
            "message": "Item added successfully",
            "wishlist": wishlist_db[user_id]
        }), 201
    except Exception as e:
        app.logger.error(f"Error in add_to_wishlist: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/wishlist', methods=['DELETE'])
def remove_from_wishlist():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_id = data.get('user_id')
        item = data.get('item')

        if not user_id or not item:
            return jsonify({"error": "user_id and item are required"}), 400

        if user_id in wishlist_db and item in wishlist_db[user_id]:
            wishlist_db[user_id].remove(item)
            return jsonify({
                "message": "Item removed successfully",
                "wishlist": wishlist_db[user_id]
            }), 200
        else:
            return jsonify({"error": "Item not found in wishlist"}), 404
    except Exception as e:
        app.logger.error(f"Error in remove_from_wishlist: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Add a health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 8206))
    host = os.environ.get("FLASK_RUN_HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
