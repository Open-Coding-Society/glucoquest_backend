import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required

# ------------------ MODEL ------------------ #
class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(255), nullable=False)
    impact = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)
    user = db.relationship('Frostbyte', backref=db.backref('food_logs', lazy=True))

    def __init__(self, meal, impact, user_id):
        self.meal = meal
        self.impact = impact
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self):
        return {
            'id': self.id,
            'meal': self.meal,
            'impact': self.impact,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id
        }


# ------------------ API ------------------ #
foodlog_api = Blueprint('foodlog_api', __name__, url_prefix='/api')
api = Api(foodlog_api)

class foodlogAPI:

    class _CRUD(Resource):
        @token_required()
        def post(self):
            current_user = g.current_user
            data = request.get_json()

            if not data or 'meal' not in data:
                return {'message': 'Meal input is required'}, 400

            meal = data['meal'].lower()

            # Basic logic for glucose impact
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
            data = request.get_json()
            if data is None or 'id' not in data:
                return {'message': 'FoodLog ID required'}, 400

            log = FoodLog.query.get(data['id'])
            if log is None:
                return {'message': 'Log not found'}, 404

            return jsonify(log.read())

        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            log = FoodLog.query.get(data['id'])

            if log is None:
                return {'message': 'Log not found'}, 404

            log.meal = data.get('meal', log.meal)
            log.impact = data.get('impact', log.impact)
            log.update()
            return jsonify(log.read())

        @token_required()
        def delete(self):
            current_user = g.current_user
            data = request.get_json()
            log = FoodLog.query.get(data['id'])

            if log is None:
                return {'message': 'Log not found'}, 404

            log.delete()
            return jsonify({"message": "Log deleted"})

    class _USER(Resource):
        @token_required()
        def get(self):
            current_user = g.current_user
            logs = FoodLog.query.filter(FoodLog.user_id == current_user.id).all()
            json_ready = [log.read() for log in logs]
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def post(self):
            logs = request.get_json()
            if not isinstance(logs, list):
                return {'message': 'Expected a list of logs'}, 400

            results = {'success_count': 0, 'error_count': 0, 'errors': []}
            with current_app.test_client() as client:
                for log in logs:
                    response = client.post('/api/foodlog', json=log)
                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['error_count'] += 1
                        results['errors'].append(response.get_json())
            return jsonify(results)

        def get(self):
            logs = FoodLog.query.all()
            return jsonify([log.read() for log in logs])

    class _FILTER(Resource):
        @token_required()
        def post(self):
            data = request.get_json()
            if not data or 'impact' not in data:
                return {'message': 'Impact value required'}, 400

            logs = FoodLog.query.filter_by(impact=data['impact']).all()
            return jsonify([log.read() for log in logs])


# ------------------ Resource Registration ------------------ #
api.add_resource(foodlogAPI._CRUD, '/foodlog')
api.add_resource(foodlogAPI._USER, '/foodlog/user')
api.add_resource(foodlogAPI._BULK_CRUD, '/foodlogs')
api.add_resource(foodlogAPI._FILTER, '/foodlogs/filter')


# ------------------ init function for main.py ------------------ #
def initfoodlog_api(app):
    app.register_blueprint(foodlog_api)