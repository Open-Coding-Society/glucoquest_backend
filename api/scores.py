from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app
from api.jwt_authorize import token_required
from model.scores import Score
from sqlalchemy import desc

score_api = Blueprint('score_api', __name__, url_prefix='/api')
api = Api(score_api)

class ScoreAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create new score (like events)"""
            data = request.get_json()
            if not data or 'points' not in data or 'level' not in data:
                return {'message': 'Missing required fields'}, 400

            score = Score(
                user_id=g.current_user.id,
                points=data['points'],
                level=data['level'],
                version=data.get('version', '1.0')
            )
            
            if not score.create():
                return {'message': 'Score creation failed'}, 500
                
            return jsonify(score.read())

        @token_required()
        def get(self):
            """Get score by ID (like events)"""
            data = request.get_json()
            if not data or 'score_id' not in data:
                return {"message": "Score ID required"}, 400

            score = Score.query.get(data['score_id'])
            if not score:
                return {"message": "Score not found"}, 404

            return jsonify(score.read())

        @token_required()
        def put(self):
            """Update score (like events)"""
            data = request.get_json()
            if not data or 'score_id' not in data:
                return {"message": "Score ID required"}, 400

            score = Score.query.get(data['score_id'])
            if not score:
                return {"message": "Score not found"}, 404

            if score.update(**data):
                return jsonify(score.read())
            return {"message": "Score update failed"}, 500

        @token_required()
        def delete(self):
            """Delete score (like events)"""
            data = request.get_json()
            if not data or 'score_id' not in data:
                return {"message": "Score ID required"}, 400

            score = Score.query.get(data['score_id'])
            if not score:
                return {"message": "Score not found"}, 404

            if score.delete():
                return {"message": "Score deleted"}
            return {"message": "Score deletion failed"}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Get all scores (like events)"""
            scores = Score.query.order_by(desc(Score.points)).all()
            return jsonify([score.read() for score in scores])

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Get scores by user (like events)"""
            scores = Score.query.filter_by(user_id=user_id).order_by(desc(Score.points)).all()
            if not scores:
                return {"message": "No scores found"}, 404
            return jsonify([score.read() for score in scores])

    class _LEADERBOARD(Resource):
        def get(self):
            """Leaderboard endpoint"""
            limit = min(int(request.args.get('limit', 10)), 100)
            scores = Score.query.order_by(desc(Score.points)).limit(limit).all()
            return jsonify([score.read() for score in scores])

# Identical endpoint registration to events
api.add_resource(ScoreAPI._CRUD, '/score')
api.add_resource(ScoreAPI._ALL, '/scores')
api.add_resource(ScoreAPI._BY_USER, '/scores/user/<int:user_id>')
api.add_resource(ScoreAPI._LEADERBOARD, '/scores/leaderboard')