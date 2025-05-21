from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from model.glucose import db, GlucoseRecord
from api.jwt_authorize import token_required

# Define Blueprint and Api
glucose_api = Blueprint('glucose_api', __name__, url_prefix='/api')
api = Api(glucose_api)

class GlucoseAPI:
    class _CRUD(Resource):
        #@token_required()
        def get(self):
            """Get all glucose records (newest first)"""
            records = GlucoseRecord.query.order_by(GlucoseRecord.time.desc()).all()
            return jsonify([
                {
                    'id': r.id,
                    'value': r.value,
                    'time': r.time.isoformat(),
                    'notes': r.notes,
                    'status': r.status,
                    'created_at': r.created_at.isoformat() if r.created_at else None
                } for r in records
            ])

        #@token_required()
        def post(self):
            """Create a new glucose record"""
            data = request.get_json()
            if not data or 'value' not in data or 'time' not in data:
                return {'error': 'Missing required fields'}, 400
            try:
                value = float(data['value'])
                if value < 1 or value > 30:
                    return {'error': 'Glucose value must be between 1 and 30 mmol/L'}, 400
                status = self.get_status(value)
                record = GlucoseRecord(
                    value=value,
                    time=datetime.fromisoformat(data['time']),
                    notes=data.get('notes', '').strip(),
                    status=status
                )
                db.session.add(record)
                db.session.commit()
                return jsonify({
                    'id': record.id,
                    'value': record.value,
                    'time': record.time.isoformat(),
                    'notes': record.notes,
                    'status': record.status,
                    'created_at': record.created_at.isoformat() if record.created_at else None
                }), 201
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 500

        #@token_required()
        def put(self):
            """Update a glucose record by id"""
            data = request.get_json()
            if not data or 'id' not in data:
                return {'error': 'Missing record id'}, 400
            record = GlucoseRecord.query.get(data['id'])
            if not record:
                return {'error': 'Record not found'}, 404
            try:
                if 'value' in data:
                    value = float(data['value'])
                    if value < 1 or value > 30:
                        return {'error': 'Glucose value must be between 1 and 30 mmol/L'}, 400
                    record.value = value
                    record.status = self.get_status(value)
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
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 500

        #@token_required()
        def delete(self):
            """Delete a glucose record by id"""
            data = request.get_json()
            if not data or 'id' not in data:
                return {'error': 'Missing record id'}, 400
            record = GlucoseRecord.query.get(data['id'])
            if not record:
                return {'error': 'Record not found'}, 404
            try:
                db.session.delete(record)
                db.session.commit()
                return {'message': 'Record deleted'}
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 500

        @staticmethod
        def get_status(value):
            if value < 4:
                return "Low"
            elif value > 7.8:
                return "High"
            return "Normal"

    class _BY_ID(Resource):
        #@token_required()
        def get(self, record_id):
            """Get a single glucose record by id"""
            record = GlucoseRecord.query.get(record_id)
            if not record:
                return {'error': 'Record not found'}, 404
            return jsonify({
                'id': record.id,
                'value': record.value,
                'time': record.time.isoformat(),
                'notes': record.notes,
                'status': record.status,
                'created_at': record.created_at.isoformat() if record.created_at else None
            })

# 注册资源
api.add_resource(GlucoseAPI._CRUD, '/glucose')
api.add_resource(GlucoseAPI._BY_ID, '/<int:record_id>')