from flask import Blueprint, request, jsonify, g
from flask_restful import Api
from flask_login import current_user, login_required
from api.jwt_authorize import token_required
from model.foodchoice import Food
from __init__ import db

# Define Blueprint and Api
food_api = Blueprint('food_api', __name__, url_prefix='/api/food')
api = Api(food_api)

# Endpoint to fetch a random suggested book (Read)
@food_api.route('/', methods=['GET'])
def get_food():
    try:
        # Query all suggested books
        foods = Food.query.all()

        # Convert the list of book objects to a list of dictionaries
        food_data = [
            {
                'number': food.number,
                'food': food.food,
                'glycemic_index': food.glycemic_index,
                'image': food.image,
            }
            for food in foods
        ]

        return jsonify(food_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch foods', 'message': str(e)}), 500