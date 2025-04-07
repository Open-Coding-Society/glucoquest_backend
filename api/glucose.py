from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.glucose import db, GlucoseRecord
from datetime import datetime

# Define Blueprint and Api
glucose_api = Blueprint('glucose_api', __name__, url_prefix='/api/glucose')
api = Api(glucose_api)

class GlucoseAPI(Resource):
    def get(self):
        """获取所有血糖记录"""
        try:
            records = GlucoseRecord.query.order_by(GlucoseRecord.time.desc()).all()
            return jsonify([record.read() for record in records])
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def post(self):
        """创建新的血糖记录"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid input: No JSON data provided"}), 400

            # 验证必填字段
            required_fields = ['value', 'time']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            # 验证血糖值范围
            value = float(data['value'])
            if value < 1 or value > 30:
                return jsonify({"error": "Glucose value must be between 1 and 30 mmol/L"}), 400

            # 确定血糖状态
            status = self._get_glucose_status(value)

            # 创建新记录
            new_record = GlucoseRecord(
                value=value,
                time=datetime.fromisoformat(data['time']),
                notes=data.get('notes', '').strip(),
                status=status
            )

            db.session.add(new_record)
            db.session.commit()
            
            return jsonify(new_record.read()), 201
        
        except ValueError as e:
            return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def put(self):
        """更新血糖记录"""
        try:
            data = request.get_json()
            if not data or 'id' not in data:
                return jsonify({"error": "Invalid input: No ID provided"}), 400

            record = GlucoseRecord.query.get(data['id'])
            if not record:
                return jsonify({"error": "Glucose record not found"}), 404

            # 更新字段
            if 'value' in data:
                value = float(data['value'])
                if value < 1 or value > 30:
                    return jsonify({"error": "Glucose value must be between 1 and 30 mmol/L"}), 400
                record.value = value
                record.status = self._get_glucose_status(value)

            if 'time' in data:
                record.time = datetime.fromisoformat(data['time'])

            if 'notes' in data:
                record.notes = data['notes'].strip()

            db.session.commit()
            return jsonify(record.read())
        except ValueError as e:
            return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def delete(self):
        """删除血糖记录"""
        try:
            data = request.get_json()
            if not data or 'id' not in data:
                return jsonify({"error": "Invalid input: No ID provided"}), 400

            record = GlucoseRecord.query.get(data['id'])
            if not record:
                return jsonify({"error": "Glucose record not found"}), 404

            db.session.delete(record)
            db.session.commit()
            return jsonify({"message": "Glucose record deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def _get_glucose_status(self, value):
        """根据血糖值确定状态"""
        if value < 4:
            return "Low"
        elif value > 7.8:
            return "High"
        return "Normal"

@glucose_api.route('/', methods=['GET'])
def get_record():
    try:
        # Query all suggested books
        records = GlucoseRecord.query.all()

        # Convert the list of book objects to a list of dictionaries
        record_data = [
            {
                'id': record.id,
                'value': record.value,
                'time': record.time,
                'notes': record.notes,
                'status': record.status,
                'created_at': record.created_at
            }
            for record in records
        ]

        return jsonify(record_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch records', 'message': str(e)}), 500

api.add_resource(GlucoseAPI, '/glucose')