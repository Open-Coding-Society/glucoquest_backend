import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import db
from api.jwt_authorize import token_required
from model.foodlog import FoodLog

# Blueprint for FoodLog API
foodlog_api = Blueprint('foodlog_api', __name__, url_prefix='/api')
api = Api(foodlog_api)

class FoodLogAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Add a new food log entry."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'meal' not in data or 'impact' not in data:
                return {"message": "Meal and impact are required"}, 400

            new_log = FoodLog(user_id=current_user.id, meal=data['meal'], impact=data['impact'])
            db.session.add(new_log)
            db.session.commit()

            return new_log.read(), 201

        @token_required()
        def get(self):
            """Retrieve all food logs for the user."""
            current_user = g.current_user
            logs = FoodLog.query.filter_by(user_id=current_user.id).all()
            return [log.read() for log in logs], 200

        @token_required()
        def delete(self):
            """Remove a food log entry."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'id' not in data:
                return {"message": "Log ID is required"}, 400

            log = FoodLog.query.filter_by(id=data['id'], user_id=current_user.id).first()
            if not log:
                return {"message": "Log not found"}, 404

            db.session.delete(log)
            db.session.commit()

            return {"message": "Log removed"}, 200

    api.add_resource(_CRUD, '/foodlog')
