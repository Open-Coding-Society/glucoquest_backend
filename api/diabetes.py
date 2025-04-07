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
            Handle POST requests to predict diabetes probability (0-1).
            Expects JSON data containing patient details.
            """
            # Get the patient data from the request
            patient = request.get_json()

            # Define and standardize patient data with all required features
            standardized_patient = {
                'HighBP': int(patient.get('highbp', 0)),
                'HighChol': int(patient.get('highchol', 0)),
                'CholCheck': int(patient.get('cholcheck', 0)),
                'BMI': float(patient.get('bmi', 25.0)),
                'Smoker': int(patient.get('smoker', 0)),
                'Stroke': int(patient.get('stroke', 0)),
                'HeartDiseaseorAttack': int(patient.get('heartdiseaseorattack', 0)),
                'PhysActivity': int(patient.get('physactivity', 0)),
                'Age': int(patient.get('age', 45)),  # Default middle age
                'GenHlth': int(patient.get('genhlth', 3)),  # Default average health
                'MentHlth': int(patient.get('menthlth', 0)),  # Default good mental health
                'PhysHlth': int(patient.get('physhlth', 0)),  # Default good physical health
                'DiffWalk': int(patient.get('diffwalk', 0)),  # Default no difficulty walking
                'Sex': int(patient.get('sex', 1)),  # Default male
                'Income': int(patient.get('income', 6))  # Default middle income
            }

            # Add BMI categories
            bmi = standardized_patient['BMI']
            standardized_patient.update({
                'BMI_Category_underweight': 1 if bmi < 18.5 else 0,
                'BMI_Category_normal': 1 if 18.5 <= bmi < 25 else 0,
                'BMI_Category_overweight': 1 if 25 <= bmi < 30 else 0,
                'BMI_Category_obese1': 1 if 30 <= bmi < 35 else 0,
                'BMI_Category_obese2': 1 if 35 <= bmi < 40 else 0,
                'BMI_Category_obese3': 1 if bmi >= 40 else 0
            })

            # Validate required fields
            required_keys = ['highbp', 'highchol', 'cholcheck', 'bmi']
            missing_keys = [key for key in required_keys if key not in patient]
            if missing_keys:
                return {'message': f'Missing required fields: {", ".join(missing_keys)}'}, 400

            # Get the model instance
            diabetes_model = DiabetesModel.get_instance()

            # Predict diabetes probability
            try:
                probability = diabetes_model.predict(standardized_patient)
                return jsonify({
                    'probability': probability,
                    'percentage': round(probability * 100, 1),
                    'risk_level': 'High' if probability > 0.7 
                                else 'Medium' if probability > 0.3 
                                else 'Low'
                })
            except Exception as e:
                return {'message': f'Error processing prediction: {str(e)}'}, 500

    class _BulkPredict(Resource):
        @token_required()
        def post(self):
            """
            Handle bulk predictions for multiple patients.
            Expects a JSON list of patient data.
            """
            patients = request.get_json()

            if not isinstance(patients, list):
                return {'message': 'Expected a list of patient data'}, 400

            results = []
            diabetes_model = DiabetesModel.get_instance()

            for patient in patients:
                try:
                    # Standardize each patient's data
                    standardized_patient = {
                        'HighBP': int(patient.get('highbp', 0)),
                        'HighChol': int(patient.get('highchol', 0)),
                        # ... include all other fields as in _Predict
                    }
                    # Add BMI categories as in _Predict
                    
                    probability = diabetes_model.predict(standardized_patient)
                    results.append({
                        'probability': probability,
                        'percentage': round(probability * 100, 1),
                        'risk_level': 'High' if probability > 0.7 
                                      else 'Medium' if probability > 0.3 
                                      else 'Low'
                    })
                except Exception as e:
                    results.append({
                        'error': f'Error processing patient: {str(e)}',
                        'patient_data': patient
                    })

            return jsonify(results)

    class _DataValidation(Resource):
        def post(self):
            """
            Validate patient data structure and types.
            """
            patient = request.get_json()

            # Required fields
            required_keys = ['highbp', 'highchol', 'cholcheck', 'bmi']
            missing_keys = [key for key in required_keys if key not in patient]
            if missing_keys:
                return {'message': f'Missing required fields: {", ".join(missing_keys)}'}, 400

            # Type validation
            type_checks = [
                ('highbp', bool, int),
                ('highchol', bool, int),
                ('cholcheck', bool, int),
                ('bmi', (int, float)),
                # Add checks for other fields if they're required
            ]

            for field, *types in type_checks:
                if field in patient and not isinstance(patient[field], types):
                    return {'message': f'Invalid type for {field}. Expected {types}'}, 400

            return {'message': 'Data is valid'}, 200

    class _FeatureWeights(Resource):
        def get(self):
            """
            Get feature importance from the model.
            """
            try:
                diabetes_model = DiabetesModel.get_instance()
                
                # If your model has a feature_weights method:
                if hasattr(diabetes_model.model, 'feature_importances_'):
                    features = diabetes_model.features
                    importances = diabetes_model.model.feature_importances_
                    weights = dict(zip(features, importances))
                    return jsonify(weights)
                else:
                    return {'message': 'Feature importance not available for this model'}, 404
            except Exception as e:
                return {'message': f'Error fetching feature weights: {str(e)}'}, 500

# Register endpoints
api.add_resource(DiabetesAPI._Predict, '/diabetes/predict')
api.add_resource(DiabetesAPI._BulkPredict, '/diabetes/bulk-predict')
api.add_resource(DiabetesAPI._DataValidation, '/diabetes/validate')
api.add_resource(DiabetesAPI._FeatureWeights, '/diabetes/feature-weights')