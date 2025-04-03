from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.diabetes import DiabetesModel
from api.jwt_authorize import token_required  # Optional, add authentication if needed

# Create a Blueprint for the Diabetes API
diabetes_api = Blueprint('diabetes_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(diabetes_api)

class DiabetesAPI:
    class _Predict(Resource):
        @token_required()  # Optional: add authentication if needed
        def post(self):
            """
            Handle POST requests to predict the diabetes status of a patient.
            Expects JSON data containing patient details.
            """
            # Get the patient data from the request
            patient = request.get_json()

            # Define correct feature names (match the training names)
            standardized_patient = {
                'HighBP': patient.get('highbp'),
                'HighChol': patient.get('highchol'),
                'CholCheck': patient.get('cholcheck'),
                'BMI': patient.get('bmi'),
                'Smoker': patient.get('smoker'),
                'Stroke': patient.get('stroke'),
                'HeartDiseaseorAttack': patient.get('heartdiseaseorattack'),
                'PhysActivity': patient.get('physactivity')
            }

            # Validate the incoming data (ensure it has the required fields)
            required_keys = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 
                             'HeartDiseaseorAttack', 'PhysActivity']
            missing_keys = [key for key in required_keys if key not in standardized_patient]
            if missing_keys:
                return {'message': f'Missing fields: {", ".join(missing_keys)}'}, 400

            # Get the singleton instance of DiabetesModel
            diabetes_model = DiabetesModel.get_instance()

            # Predict the diabetes status of the patient
            try:
                response = diabetes_model.predict(standardized_patient)
                return jsonify({'prediction': response})
            except Exception as e:
                return {'message': f'Error processing prediction: {str(e)}'}, 500

    class _BulkPredict(Resource):
        """
        Bulk operation for predicting diabetes status for multiple patients.
        """

        @token_required()  # Optional: add authentication if needed
        def post(self):
            """
            Handle POST requests for bulk predictions.
            Expects a JSON list of patient data.
            """
            patients = request.get_json()

            if not isinstance(patients, list):
                return {'message': 'Expected a list of patient data'}, 400

            predictions = []
            for patient in patients:
                try:
                    response = DiabetesModel.get_instance().predict(patient)
                    predictions.append({'prediction': response[0]})
                except Exception as e:
                    predictions.append({'error': f'Error processing patient: {str(e)}'})

            return jsonify(predictions)

    class _DataValidation(Resource):
        """
        Endpoint for validating patient data schema.
        """

        def post(self):
            """
            Validate incoming patient data.
            Checks for required fields and correct types.
            """
            patient = request.get_json()

            required_keys = ['highbp', 'highchol', 'cholcheck', 'bmi', 'smoker', 'stroke', 
                             'heartdiseaseorattack', 'physactivity']
            missing_keys = [key for key in required_keys if key not in patient]
            if missing_keys:
                return {'message': f'Missing fields: {", ".join(missing_keys)}'}, 400

            # Additional checks can be added here for data type validation, e.g., numeric checks for 'bmi'
            if not isinstance(patient['bmi'], (int, float)):
                return {'message': 'Invalid data type for BMI'}, 400

            return {'message': 'Data is valid'}, 200

    class _FeatureWeights(Resource):
        """
        Endpoint for retrieving feature importance (weights) from the Diabetes model.
        """

        def get(self):
            """
            Handle GET requests to retrieve the feature weights.
            Returns the feature importance of each feature in the model.
            """
            try:
                # Get the singleton instance of DiabetesModel
                diabetes_model = DiabetesModel.get_instance()

                # Fetch the feature weights (optional, if you have this functionality in your model)
                # Example: If you have a method in the model to retrieve feature weights, you can use it here
                feature_weights = diabetes_model.feature_weights()

                # Return the feature weights as a JSON response
                return jsonify(feature_weights)
            except Exception as e:
                return {'message': f'Error fetching feature weights: {str(e)}'}, 500

# Register the API resources with the Blueprint
api.add_resource(DiabetesAPI._Predict, '/diabetes/predict')
api.add_resource(DiabetesAPI._BulkPredict, '/diabetes/bulk-predict')
api.add_resource(DiabetesAPI._DataValidation, '/diabetes/validate')
api.add_resource(DiabetesAPI._FeatureWeights, '/diabetes/feature-weights')
