import base64
from flask import Blueprint, request, jsonify, g
from flask_restful import Api
from flask_login import current_user, login_required
from api.jwt_authorize import token_required
from model.foodchoice import Food
from __init__ import db

# Define Blueprint and Api
food_api = Blueprint('food_api', __name__, url_prefix='/api/foodchoice')
api = Api(food_api)

# Helper function to convert image to Base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        return None

@food_api.route('/', methods=['GET'])
def get_food():
    try:
        pair_number = request.args.get('number', type=int)

        # Query all foods
        foods = Food.query.all()

        # Group foods by number
        food_dict = {}
        for food in foods:
            food_dict.setdefault(food.number, []).append(food)

        # Use the number if provided, otherwise pick first valid pair
        if pair_number:
            selected_foods = food_dict.get(pair_number, [])[:2]
        else:
            selected_foods = next((foods[:2] for foods in food_dict.values() if len(foods) >= 2), [])

        # If no foods matched (e.g. number too high), return empty
        if not selected_foods:
            return jsonify([]), 200

        # Convert to JSON
        food_data = [
            {
                'number': food.number,
                'food': food.food,
                'glycemic_load': food.glycemic_load,
                'info': food.info,
                'image': f"/images/food/{food.image}" if food.image else None
            }
            for food in selected_foods
        ]

        return jsonify(food_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch foods', 'message': str(e)}), 500

@food_api.route('/info', methods=['GET'])
def get_food_info():
    food_name = request.args.get('food', type=str)
    food = Food.query.filter_by(food=food_name).first()
    if food:
        return jsonify({'info': food.info})
    return jsonify({'info': 'No info found'}), 404
