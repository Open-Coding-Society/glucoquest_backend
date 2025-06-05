from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
from __init__ import db
from model.survey import Survey
from api.jwt_authorize import token_required

survey_api = Blueprint('survey_api', __name__, url_prefix='/api')
api = Api(survey_api)

class SurveyAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new survey response with optional name."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'message' not in data:
                return {'message': 'Survey message is required'}, 400

            # Create a new Survey response with optional name
            survey_response = Survey(
                message=data['message'],
                user_id=current_user.id,
                name=data.get('name')  # Optional field
            )

            try:
                survey_response.create()
                return survey_response.read(), 201
            except IntegrityError:
                return {'message': 'Survey creation failed'}, 500

        @token_required()
        def get(self):
            """Retrieve a survey response by ID with name included."""
            survey_id = request.args.get('id')
            if not survey_id:
                return {'message': 'Survey ID required'}, 400

            survey_response = Survey.query.get(survey_id)
            if not survey_response:
                return {'message': 'Survey not found'}, 404

            return {
                **survey_response.read(),
                'author': f'"{survey_response.message}" - {survey_response.name or "Anonymous"}'
            }

        @token_required()
        def put(self):
            """Update an existing survey response including name."""
            survey_id = request.args.get('id')
            data = request.get_json()

            if not survey_id:
                return {'message': 'Survey ID required'}, 400
            if not data or 'message' not in data:
                return {'message': 'Updated message is required'}, 400

            survey_response = Survey.query.get(survey_id)
            if not survey_response:
                return {'message': 'Survey not found'}, 404

            try:
                survey_response.message = data['message']
                if 'name' in data:
                    survey_response.name = data['name']
                survey_response.update()
                return {
                    'message': 'Survey updated',
                    'data': survey_response.read(),
                    'formatted': f'"{data["message"]}" - {data.get("name", "Anonymous")}'
                }, 200
            except IntegrityError:
                return {'message': 'Update failed'}, 500

        @token_required()
        def delete(self):
            """Delete a survey response by ID."""
            survey_id = request.args.get('id')
            if not survey_id:
                return {'message': 'Survey ID required'}, 400

            survey_response = Survey.query.get(survey_id)
            if not survey_response:
                return {'message': 'Survey not found'}, 404

            try:
                survey_response.delete()
                return {'message': 'Survey deleted'}, 200
            except IntegrityError:
                return {'message': 'Deletion failed'}, 500

    class _ALL(Resource):
        def get(self):
            """Retrieve all survey responses with formatted author info."""
            surveys = Survey.query.all()
            if not surveys:
                return {'message': 'No surveys found'}, 404

            return [{
                **survey.read(),
                'author': f'"{survey.message}" - {survey.name or "Anonymous"}'
            } for survey in surveys]

    class _PUBLIC(Resource):
        def get(self):
            """Public endpoint to get surveys without auth (read-only)"""
            surveys = Survey.query.limit(100).all()  # Limit for public safety
            return [{
                'id': s.id,
                'content': f'"{s.message}" - {s.name or "Anonymous"}',
                'timestamp': s.created_at.isoformat() if hasattr(s, 'created_at') else None
            } for s in surveys]

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Get surveys by user with formatted output"""
            surveys = Survey.query.filter_by(user_id=user_id).all()
            return [{
                'id': s.id,
                'message': s.message,
                'name': s.name,
                'formatted': f'"{s.message}" - {s.name or "Anonymous"}',
                'timestamp': s.created_at.isoformat() if hasattr(s, 'created_at') else None
            } for s in surveys]

# Register endpoints
api.add_resource(SurveyAPI._CRUD, '/survey')
api.add_resource(SurveyAPI._ALL, '/surveys')
api.add_resource(SurveyAPI._PUBLIC, '/surveys/public')  # New public endpoint
api.add_resource(SurveyAPI._BY_USER, '/surveys/user/<int:user_id>')