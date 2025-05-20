from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db

class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    meal = db.Column(db.String(255), nullable=False)
    impact = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, meal, impact):
        self.user_id = user_id
        self.meal = meal
        self.impact = impact

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "meal": self.meal,
            "impact": self.impact,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Seeder
def initFoodLogs():
    sample_logs = [
        {"user_id": 1, "meal": "banana and toast", "impact": "Medium"},
        {"user_id": 2, "meal": "salad and chicken", "impact": "Low"},
        {"user_id": 3, "meal": "ice cream and soda", "impact": "High"},
    ]
    for data in sample_logs:
        log = FoodLog(user_id=data["user_id"], meal=data["meal"], impact=data["impact"])
        db.session.add(log)
    db.session.commit()
