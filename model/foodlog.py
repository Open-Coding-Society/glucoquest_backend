from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from __init__ import db


class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(255), nullable=False)
    impact = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)
    user = relationship('Frostbyte', backref='food_logs')  # assuming user table is Frostbyte

    def __init__(self, meal, impact, user_id):
        self.meal = meal
        self.impact = impact
        self.user_id = user_id

    def create(self):
        """Save the FoodLog entry to the database."""
        db.session.add(self)
        db.session.commit()

    def read(self):
        """Convert the FoodLog object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "meal": self.meal,
            "impact": self.impact,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id
        }

    def update(self):
        """Update the FoodLog entry in the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the FoodLog entry from the database."""
        db.session.delete(self)
        db.session.commit()


# ------------------ Sample Seeder ------------------ #
def initFoodLogs():
    from model.foodlog import FoodLog  # avoid circular imports
    sample_logs = [
        {"meal": "banana and toast", "impact": "Medium", "user_id": 1},
        {"meal": "salad and chicken", "impact": "Low", "user_id": 2},
        {"meal": "ice cream and soda", "impact": "High", "user_id": 3},
    ]
    for data in sample_logs:
        log = FoodLog(meal=data["meal"], impact=data["impact"], user_id=data["user_id"])
        db.session.add(log)
    db.session.commit()
