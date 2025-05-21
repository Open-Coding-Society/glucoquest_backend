from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from sqlalchemy import desc
from __init__ import app
from api.jwt_authorize import token_required
from model.scores import Score

# Create a Blueprint for the score API
score_api = Blueprint('score_api', __name__, url_prefix='/api')
api = Api(score_api)

class ScoreAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new score."""
            current_user = g.current_user
            data = request.get_json()

            if not data:
                return {'message': 'No input data provided'}, 400
            if 'points' not in data or 'level' not in data:
                return {'message': 'Points and level are required'}, 400

            score = Score(
                user_id=current_user.id,
                points=data['points'],
                level=data['level'],
                version=data.get('version', '1.0')
            )

            if not score.create():
                return {'message': 'Score creation failed'}, 500

            return jsonify(score.read())

        @token_required()
        def get(self):
            """Retrieve a score by ID."""
            data = request.get_json()
            if not data or 'score_id' not in data:
                return {"message": "Score ID required"}, 400

            score = Score.query.get(data['score_id'])
            if not score:
                return {"message": "Score not found"}, 404

            return jsonify(score.read())

        @token_required()
        def put(self):
            """Update an existing score."""
            data = request.get_json()
            if not data or 'score_id' not in data:
                return {"message": "Score ID required"}, 400

            score = Score.query.get(data['score_id'])
            if not score:
                return {"message": "Score not found"}, 404

            try:
                if 'points' in data:
                    score.points = data['points']
                if 'level' in data:
                    score.level = data['level']
                if 'version' in data:
                    score.version = data['version']

                score.update()
                return jsonify(score.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete a score."""
            data = request.get_json()
            if not data or 'score_id' not in data:
                return {"message": "Score ID required"}, 400

            score = Score.query.get(data['score_id'])
            if not score:
                return {"message": "Score not found"}, 404

            try:
                score.delete()
                return {"message": "Score deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all scores."""
            scores = Score.query.order_by(desc(Score.points)).all()
            return jsonify([score.read() for score in scores])

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Retrieve scores by user ID."""
            scores = Score.query.filter_by(user_id=user_id).order_by(desc(Score.points)).all()
            if not scores:
                return {"message": "No scores found for this user."}, 404
            return jsonify([score.read() for score in scores])

    class _LEADERBOARD(Resource):
        def get(self):
            """Retrieve top scores (leaderboard)."""
            try:
                limit = int(request.args.get('limit', 10))
                limit = min(limit, 100)  # cap at 100
            except ValueError:
                return {"message": "Invalid limit value"}, 400

            scores = Score.query.order_by(desc(Score.points)).limit(limit).all()
            return jsonify([score.read() for score in scores])

# Register API endpoints
api.add_resource(ScoreAPI._CRUD, '/score')
api.add_resource(ScoreAPI._ALL, '/scores')
api.add_resource(ScoreAPI._BY_USER, '/scores/user/<int:user_id>')
api.add_resource(ScoreAPI._LEADERBOARD, '/scores/leaderboard')
