from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.foodlog import FoodLog

foodlog_api = Blueprint('foodlog_api', __name__, url_prefix='/api')
api = Api(foodlog_api)

class FoodLogAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            current_user = g.current_user
            data = request.get_json()
            meal = data.get("meal", "").lower()

            if not meal:
                return {'message': 'Meal is required'}, 400

            high = ["candy", "soda", "ice cream"]
            medium = ["banana", "bread", "rice"]
            low = ["chicken", "salad", "eggs"]

            impact = "Unknown"
            for word in meal.split():
                if word in high:
                    impact = "High"
                    break
                elif word in medium:
                    impact = "Medium"
                    break
                elif word in low:
                    impact = "Low"
                    break

            log = FoodLog(meal=meal, impact=impact, user_id=current_user.id)
            log.create()
            return jsonify(log.read())

        @token_required()
        def get(self):
            current_user = g.current_user
            logs = FoodLog.query.filter_by(user_id=current_user.id).all()
            return jsonify([log.read() for log in logs])

    api.add_resource(_CRUD, '/foodlog')
