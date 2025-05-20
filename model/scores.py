from __init__ import app, db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import logging

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)  # Changed from 'score' to match your pattern
    level = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Changed from date_achieved
    version = db.Column(db.String(20), default='1.0')  # Changed from game_version

    # Relationship (exactly like Events)
    user = db.relationship('User', backref='scores')

    def __init__(self, user_id, points, level, version='1.0'):
        self.user_id = user_id
        self.points = points
        self.level = level
        self.version = version

    def __repr__(self):
        return f'Score(id={self.id}, user={self.user_id}, points={self.points})'

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error creating score: {str(e)}")
            return None

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "points": self.points,
            "level": self.level,
            "created": self.created.isoformat(),
            "version": self.version
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error updating score: {str(e)}")
            return None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error deleting score: {str(e)}")
            return False

def init_scores():
    """Initialize sample scores (like your events)"""
    with app.app_context():
        db.create_all()
        samples = [
            (1, 1500, 3),
            (2, 2200, 5),
            (3, 800, 2)
        ]
        for user_id, points, level in samples:
            score = Score(
                user_id=user_id,
                points=points,
                level=level
            )
            try:
                db.session.add(score)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()