from __init__ import db
from datetime import datetime

class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(255), nullable=False)
    impact = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, meal, impact, user_id):
        self.meal = meal
        self.impact = impact
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            'id': self.id,
            'meal': self.meal,
            'impact': self.impact,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }
