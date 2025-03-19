from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from model.titanic import TitanicModel
from api.jwt_authorize import token_required

# Create a Blueprint for the Titanic API
titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(titanic_api)

class TitanicAPI:
    """
    Define the API endpoints for Titanic model.
    """
    class _Predict(Resource):
        """
        Titanic API operation for making survival predictions.
        """

        @token_required()  # Optional: add authentication if needed
        def post(self):
            """
            Handle POST requests to predict the survival of a passenger.
            Expects JSON data containing passenger details.
            """
            # Get the passenger data from the request
            passenger = request.get_json()

            # Validate the incoming data (ensure it has the required fields)
            required_keys = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
            missing_keys = [key for key in required_keys if key not in passenger]
            if missing_keys:
                return {'message': f'Missing fields: {", ".join(missing_keys)}'}, 400

            # Get the singleton instance of TitanicModel
            titanic_model = TitanicModel.get_instance()

            # Predict the survival probability of the passenger
            try:
                response = titanic_model.predict(passenger)
                return jsonify(response)
            except Exception as e:
                return {'message': f'Error processing prediction: {str(e)}'}, 500

    class _BulkPredict(Resource):
        """
        Bulk operation for predicting survival for multiple passengers.
        """

        @token_required()  # Optional: add authentication if needed
        def post(self):
            """
            Handle POST requests for bulk predictions.
            Expects a JSON list of passenger data.
            """
            passengers = request.get_json()

            if not isinstance(passengers, list):
                return {'message': 'Expected a list of passenger data'}, 400

            predictions = []
            for passenger in passengers:
                try:
                    response = TitanicModel.get_instance().predict(passenger)
                    predictions.append(response)
                except Exception as e:
                    predictions.append({'error': f'Error processing passenger: {str(e)}'})

            return jsonify(predictions)

    class _DataValidation(Resource):
        """
        Endpoint for validating passenger data schema.
        """

        def post(self):
            """
            Validate incoming passenger data.
            Checks for required fields and correct types.
            """
            passenger = request.get_json()

            required_keys = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
            missing_keys = [key for key in required_keys if key not in passenger]
            if missing_keys:
                return {'message': f'Missing fields: {", ".join(missing_keys)}'}, 400

            # Additional checks can be added here for data type validation, e.g., numeric checks for 'Age'
            if not isinstance(passenger['Age'], (int, float)):
                return {'message': 'Invalid data type for Age'}, 400

            return {'message': 'Data is valid'}, 200

# Register the API resources with the Blueprint
api.add_resource(TitanicAPI._Predict, '/titanic/predict')
api.add_resource(TitanicAPI._BulkPredict, '/titanic/bulk-predict')
api.add_resource(TitanicAPI._DataValidation, '/titanic/validate')
