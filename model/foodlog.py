from __init__ import db
from datetime import datetime

class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(255), nullable=False)
    impact = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, nullable=False)  # ✅ no ForeignKey if you don’t have a user table

    def __init__(self, meal, impact, user_id):
        self.meal = meal
        self.impact = impact
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "meal": self.meal,
            "impact": self.impact,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id
        }

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
