from flask_restful import Api, Resource
from sqlalchemy import Text, JSON
from __init__ import app, db
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlite3 import IntegrityError
from datetime import datetime

class DiabetesPrediction(db.Model):
    __tablename__ = 'diabetes_predictions'
    
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(String(80), nullable=False)
    probability = db.Column(Float, nullable=False)
    risk_level = db.Column(String(20), nullable=False)
    high_bp = db.Column(Integer)
    high_chol = db.Column(Integer)
    bmi = db.Column(Float)
    age = db.Column(Integer)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    input_features = db.Column(JSON)

    def __repr__(self):
        return f"<DiabetesPrediction(id={self.id}, user_id={self.user_id}, probability={self.probability}, risk_level={self.risk_level})>"

    # CRUD methods
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'probability': self.probability,
            'risk_level': self.risk_level,
            'high_bp': self.high_bp,
            'high_chol': self.high_chol,
            'bmi': self.bmi,
            'age': self.age,
            'timestamp': self.timestamp.isoformat(),
            'input_features': self.input_features
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self
            
        self.user_id = inputs.get('user_id', self.user_id)
        self.probability = inputs.get('probability', self.probability)
        self.risk_level = inputs.get('risk_level', self.risk_level)
        self.high_bp = inputs.get('high_bp', self.high_bp)
        self.high_chol = inputs.get('high_chol', self.high_chol)
        self.bmi = inputs.get('bmi', self.bmi)
        self.age = inputs.get('age', self.age)
        self.input_features = inputs.get('input_features', self.input_features)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        restored_predictions = {}

        for prediction_data in data:
            prediction_data.pop('id', None)
            
            existing_prediction = DiabetesPrediction.query.filter_by(
                user_id=prediction_data.get('user_id'),
                timestamp=prediction_data.get('timestamp')
            ).first()

            if existing_prediction:
                for key, value in prediction_data.items():
                    setattr(existing_prediction, key, value)

                try:
                    db.session.commit()
                    restored_predictions[existing_prediction.id] = {
                        'status': 'updated',
                        'prediction': existing_prediction.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_predictions[existing_prediction.id] = {
                        'status': 'error',
                        'message': str(e)
                    }
            else:
                new_prediction = DiabetesPrediction(**prediction_data)
                db.session.add(new_prediction)
                try:
                    db.session.commit()
                    restored_predictions[new_prediction.id] = {
                        'status': 'created',
                        'prediction': new_prediction.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_predictions[new_prediction.id] = {
                        'status': 'error',
                        'message': str(e)
                    }

        return restored_predictions

def initPredictions():
    """Initialize with sample predictions if needed"""
    sample_predictions = [
        {
            "user_id": "test_user_1",
            "probability": 0.65,
            "risk_level": "Medium",
            "high_bp": 1,
            "high_chol": 0,
            "bmi": 28.5,
            "age": 45,
            "input_features": {
                "HighBP": 1,
                "HighChol": 0,
                "BMI": 28.5,
                "Age": 45
            }
        },
        {
            "user_id": "test_user_2",
            "probability": 0.82,
            "risk_level": "High",
            "high_bp": 1,
            "high_chol": 1,
            "bmi": 32.1,
            "age": 52,
            "input_features": {
                "HighBP": 1,
                "HighChol": 1,
                "BMI": 32.1,
                "Age": 52
            }
        }
    ]

    for pred in sample_predictions:
        if not DiabetesPrediction.query.filter_by(
            user_id=pred["user_id"],
            timestamp=datetime.fromisoformat(pred.get("timestamp", "2023-01-01T00:00:00"))
        ).first():
            new_pred = DiabetesPrediction(
                user_id=pred["user_id"],
                probability=pred["probability"],
                risk_level=pred["risk_level"],
                high_bp=pred["high_bp"],
                high_chol=pred["high_chol"],
                bmi=pred["bmi"],
                age=pred["age"],
                input_features=pred["input_features"]
            )
            db.session.add(new_pred)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("IntegrityError: Possible duplicate prediction")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing predictions: {e}")

with app.app_context():
    db.create_all()
    initPredictions()  # Comment this out after first run if you don't want sample data