from __init__ import app, db
import logging
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

class GlucoseRecord(db.Model):
    __tablename__ = 'glucose_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(500), default='')
    status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='glucose_records')

    def __init__(self, user_id, value, time, notes=''):
        self.user_id = user_id
        self.value = float(value)
        self.time = time if isinstance(time, datetime) else datetime.fromisoformat(time)
        self.notes = notes
        self.status = self._calculate_status(self.value)

    def __repr__(self):
        return f'GlucoseRecord(id={self.id}, user={self.user_id}, value={self.value})'

    @staticmethod
    def _calculate_status(value):
        value = float(value)
        if value < 4: return "Low"
        if value > 7.8: return "High"
        return "Normal"

    def create(self):
        try:
            if not 1 <= self.value <= 30:
                raise ValueError("Glucose value must be between 1-30 mmol/L")
            db.session.add(self)
            db.session.commit()
            return self
        except (IntegrityError, ValueError) as e:
            db.session.rollback()
            logging.error(f"Error creating glucose record: {str(e)}")
            return None
        
    def read(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.name if self.user else f"User {self.user_id}",
            'value': self.value,
            'time': self.time.isoformat(),
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
        
    def update(self, **kwargs):
        try:
            if 'value' in kwargs:
                value = float(kwargs['value'])
                if not 1 <= value <= 30:
                    raise ValueError("Glucose value must be between 1-30 mmol/L")
                self.value = value
                self.status = self._calculate_status(value)
                
            if 'time' in kwargs:
                self.time = kwargs['time'] if isinstance(kwargs['time'], datetime) else datetime.fromisoformat(kwargs['time'])
                
            if 'notes' in kwargs:
                self.notes = kwargs['notes']
                
            db.session.commit()
            return self
        except (IntegrityError, ValueError) as e:
            db.session.rollback()
            logging.error(f"Error updating glucose record: {str(e)}")
            return None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error deleting glucose record: {str(e)}")
            return False



def init_glucose():
    """Initialize sample glucose records"""
    with app.app_context():
        db.create_all()
        if not GlucoseRecord.query.first():
            samples = [
                (1, 5.2, datetime.utcnow() - timedelta(days=2), "Morning fasting"),
                (2, 7.1, datetime.utcnow() - timedelta(days=1, hours=2), "After lunch"), 
                (1, 4.8, datetime.utcnow() - timedelta(hours=3), "Evening check")
            ]
            for user_id, value, time, notes in samples:
                record = GlucoseRecord(
                    user_id=user_id,
                    value=value,
                    time=time,
                    notes=notes
                )
                try:
                    db.session.add(record)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    logging.warning("Error seeding glucose records")