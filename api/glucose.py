from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.glucose import GlucoseRecord

# Create a Blueprint for the glucose API
glucose_api = Blueprint('glucose_api', __name__, url_prefix='/api')
api = Api(glucose_api)

class GlucoseAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            data = request.get_json()
            try:
                record = GlucoseRecord(
                    user_id=g.current_user.id,  # or data['user_id'] if different
                    value=data['value'],
                    time=data.get('time', datetime.utcnow().isoformat()),
                    notes=data.get('notes', '')
                    # Don't include status here
                )
                if record.create():
                    return jsonify(record.read())
                return {'message': 'Failed to create record'}, 400
            except Exception as e:
                return {'message': str(e)}, 400
        @token_required()
        def get(self):
            """Get user's glucose records"""
            records = GlucoseRecord.query.filter_by(user_id=g.current_user.id)\
                            .order_by(GlucoseRecord.time.desc()).all()
            return jsonify([r.read() for r in records])

        @token_required()
        def put(self):
            """Update an existing glucose record."""
            data = request.get_json()
            if not data or 'record_id' not in data:
                return {"message": "Record ID required"}, 400

            record = GlucoseRecord.query.get(data['record_id'])
            if not record:
                return {"message": "Record not found"}, 404

            try:
                if 'value' in data:
                    value = float(data['value'])
                    if value < 1 or value > 30:
                        return {'message': 'Glucose value must be between 1 and 30 mmol/L'}, 400
                    record.value = value
                    record.status = self._get_status(value)
                if 'time' in data:
                    record.time = datetime.fromisoformat(data['time'])
                if 'notes' in data:
                    record.notes = data['notes'].strip()

                record.update()
                return jsonify(record.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete a glucose record."""
            data = request.get_json()
            if not data or 'record_id' not in data:
                return {"message": "Record ID required"}, 400

            record = GlucoseRecord.query.get(data['record_id'])
            if not record:
                return {"message": "Record not found"}, 404

            try:
                record.delete()
                return {"message": "Record deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

        @staticmethod
        def _get_status(value):
            if value < 4:
                return "Low"
            elif value > 7.8:
                return "High"
            return "Normal"

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all glucose records (newest first)."""
            records = GlucoseRecord.query.order_by(GlucoseRecord.time.desc()).all()
            return jsonify([record.read() for record in records])

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Retrieve glucose records by user ID."""
            records = GlucoseRecord.query.filter_by(user_id=user_id).order_by(GlucoseRecord.time.desc()).all()
            if not records:
                return {"message": "No records found for this user."}, 404
            return jsonify([record.read() for record in records])

    class _RECENT(Resource):
        @token_required()
        def get(self):
            """Retrieve recent glucose records."""
            try:
                limit = int(request.args.get('limit', 10))
                limit = min(limit, 100)  # cap at 100
            except ValueError:
                return {"message": "Invalid limit value"}, 400

            records = GlucoseRecord.query.order_by(GlucoseRecord.time.desc()).limit(limit).all()
            return jsonify([record.read() for record in records])

# Register API endpoints
api.add_resource(GlucoseAPI._CRUD, '/glucose')
api.add_resource(GlucoseAPI._ALL, '/glucose/all')
api.add_resource(GlucoseAPI._BY_USER, '/glucose/user/<int:user_id>')
api.add_resource(GlucoseAPI._RECENT, '/glucose/recent')