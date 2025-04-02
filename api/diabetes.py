from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from diabetes import DiabetesModel
# from api.jwt_authorize import token_required  # Uncomment if you want to add token-based authorization

# Create a Blueprint for the Diabetes API
diabetes_api = Blueprint('diabetes_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(diabetes_api)

class DiabetesAPI:
    """
    Define the API endpoints for the Diabetes model.
    """

    class _Predict(Resource):
        """
        Diabetes API operation for predicting the likelihood of diabetes.
        """

        # @token_required()  # Uncomment to add authentication if needed
        def post(self):
            """
            Handle POST requests to predict the likelihood of diabetes.
            Expects JSON data containing glucose, BMI, age, insulin, and blood pressure.
            """
            data = request.get_json()

            # Validate the incoming data (ensure it has the required fields)
            required_keys = ['Glucose', 'BMI', 'Age', 'Insulin', 'BloodPressure']
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                return {'message': f'Missing fields: {", ".join(missing_keys)}'}, 400

            # Get the singleton instance of the DiabetesModel
            model = DiabetesModel.get_instance()

            # Make prediction
            prediction = model.predict([data['Glucose'], data['BMI'], data['Age'],
                                        data['Insulin'], data['BloodPressure']])

            return jsonify({'prediction': prediction})

    class _Probability(Resource):
        """
        Diabetes API operation for getting the probability of diabetes.
        """

        # @token_required()  # Uncomment to add authentication if needed
        def post(self):
            """
            Handle POST requests to get the probability of diabetes.
            Expects JSON data containing glucose, BMI, age, insulin, and blood pressure.
            """
            data = request.get_json()

            # Validate the incoming data (ensure it has the required fields)
            required_keys = ['Glucose', 'BMI', 'Age', 'Insulin', 'BloodPressure']
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                return {'message': f'Missing fields: {", ".join(missing_keys)}'}, 400

            # Get the singleton instance of the DiabetesModel
            model = DiabetesModel.get_instance()

            # Get the prediction probabilities
            probability = model.predict_proba([data['Glucose'], data['BMI'], data['Age'],
                                               data['Insulin'], data['BloodPressure']])

            return jsonify({'probability': {'no_diabetes': probability[0], 'diabetes': probability[1]}})

    class _FeatureImportance(Resource):
        """
        Diabetes API operation for retrieving feature importance.
        """

        # @token_required()  # Uncomment to add authentication if needed
        def get(self):
            """
            Handle GET requests to retrieve the feature importance.
            """
            model = DiabetesModel.get_instance()
            feature_importance = model.feature_importance()

            return jsonify({'feature_importance': feature_importance})

# Register the API resources with the Blueprint
api.add_resource(DiabetesAPI._Predict, '/diabetes/predict')
api.add_resource(DiabetesAPI._Probability, '/diabetes/probability')
api.add_resource(DiabetesAPI._FeatureImportance, '/diabetes/feature-importance')
