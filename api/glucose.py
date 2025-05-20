from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from datetime import datetime
from model.glucose import db, GlucoseRecord

# Define Blueprint and Api
glucose_api = Blueprint('glucose_api', __name__, url_prefix='/api/glucose')
api = Api(glucose_api)

@glucose_api.route('/', methods=['GET'])
def get_records():
    try:
        # Query all glucose records ordered by time (newest first)
        records = GlucoseRecord.query.order_by(GlucoseRecord.time.desc()).all()

        # Convert the list of record objects to a list of dictionaries
        record_data = [
            {
                'id': record.id,
                'value': record.value,
                'time': record.time.isoformat(),
                'notes': record.notes,
                'status': record.status,
                'created_at': record.created_at.isoformat() if record.created_at else None
            }
            for record in records
        ]

        return jsonify(record_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch records', 'message': str(e)}), 500

@glucose_api.route('/', methods=['POST'])
def create_record():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input: No JSON data provided"}), 400

        required_fields = ['value', 'time']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        value = float(data['value'])
        if value < 1 or value > 30:
            return jsonify({"error": "Glucose value must be between 1 and 30 mmol/L"}), 400

        status = "Low" if value < 4 else "High" if value > 7.8 else "Normal"

        new_record = GlucoseRecord(
            value=value,
            time=data['time'], 
            notes=data.get('notes', '').strip()
        )

        new_record.status = status

        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({
            'id': new_record.id,
            'value': new_record.value,
            'time': new_record.time.isoformat(),
            'notes': new_record.notes,
            'status': new_record.status,
            'created_at': new_record.created_at.isoformat() if new_record.created_at else None
        }), 201
    
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@glucose_api.route('/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input: No JSON data provided"}), 400

        record = GlucoseRecord.query.get(record_id)
        if not record:
            return jsonify({"error": "Glucose record not found"}), 404

        if 'value' in data:
            value = float(data['value'])
            if value < 1 or value > 30:
                return jsonify({"error": "Glucose value must be between 1 and 30 mmol/L"}), 400
            record.value = value
            record.status = get_glucose_status(value)

        if 'time' in data:
            record.time = datetime.fromisoformat(data['time'])

        if 'notes' in data:
            record.notes = data['notes'].strip()

        db.session.commit()
        return jsonify({
            'id': record.id,
            'value': record.value,
            'time': record.time.isoformat(),
            'notes': record.notes,
            'status': record.status,
            'created_at': record.created_at.isoformat() if record.created_at else None
        })
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@glucose_api.route('/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        record = GlucoseRecord.query.get(record_id)
        if not record:
            return jsonify({"error": "Glucose record not found"}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Glucose record deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def get_glucose_status(value):
    if value < 4:
        return "Low"
    elif value > 7.8:
        return "High"
    return "Normal"