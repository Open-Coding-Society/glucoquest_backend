import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.prediction import DiabetesPrediction  # Import the DiabetesPrediction model

# Create a Blueprint for the prediction API
prediction_api = Blueprint('prediction_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(prediction_api)

class PredictionAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new diabetes prediction."""
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'probability' not in data:
                return {'message': 'Probability is required'}, 400
            if 'risk_level' not in data:
                return {'message': 'Risk level is required'}, 400

            # Create a DiabetesPrediction instance
            prediction = DiabetesPrediction(
                user_id=current_user.id,  # Attach the current user ID to the prediction
                probability=data['probability'],
                risk_level=data['risk_level']
            )

            # Save the prediction object using the ORM method defined in the model
            prediction.create()
            return jsonify(prediction.read())

        @token_required()
        def get(self):
            """Retrieve a specific prediction by ID."""
            data = request.get_json()
            if not data or 'prediction_id' not in data:
                return {"message": "Prediction ID required"}, 400

            prediction = DiabetesPrediction.query.get(data['prediction_id'])
            if not prediction:
                return {"message": "Prediction not found"}, 404

            return jsonify(prediction.read())

        @token_required()
        def put(self):
            """Update an existing diabetes prediction."""
            data = request.get_json()
            if not data or 'prediction_id' not in data:
                return {"message": "Prediction ID required"}, 400

            prediction = DiabetesPrediction.query.get(data['prediction_id'])
            if not prediction:
                return {"message": "Prediction not found"}, 404

            try:
                if 'probability' in data:
                    prediction.probability = data['probability']
                if 'risk_level' in data:
                    prediction.risk_level = data['risk_level']

                prediction.update()
                return jsonify(prediction.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete a diabetes prediction."""
            data = request.get_json()
            if not data or 'prediction_id' not in data:
                return {"message": "Prediction ID required"}, 400

            prediction = DiabetesPrediction.query.get(data['prediction_id'])
            if not prediction:
                return {"message": "Prediction not found"}, 404

            try:
                prediction.delete()
                return {"message": "Prediction deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all diabetes predictions."""
            predictions = DiabetesPrediction.query.all()
            return jsonify([prediction.read() for prediction in predictions])

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Retrieve predictions by user ID."""
            predictions = DiabetesPrediction.query.filter_by(user_id=user_id).all()  # Filter predictions by user_id
            if not predictions:
                return {"message": "No predictions found for this user."}, 404
            return jsonify([prediction.read() for prediction in predictions])

# Map API endpoints
api.add_resource(PredictionAPI._CRUD, '/prediction')
api.add_resource(PredictionAPI._ALL, '/predictions')
api.add_resource(PredictionAPI._BY_USER, '/predictions/user/<int:user_id>')  # New endpoint to get predictions by user ID
