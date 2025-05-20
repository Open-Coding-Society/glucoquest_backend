from __init__ import app, db
import logging
from datetime import datetime

class GlucoseRecord(db.Model):
    __tablename__ = 'glucose_records'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(500))
    status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, value, time, notes=None, _skip_status=False):
        self.value = float(value)
        self.time = time if isinstance(time, datetime) else datetime.fromisoformat(time)
        self.notes = notes or ""
        
        if not _skip_status:
            self.status = self._calculate_status(self.value)

    @staticmethod
    def _calculate_status(value):
        value = float(value)
        if value < 4: return "Low"
        if value > 7.8: return "High"
        return "Normal"

    def create(self):
        try:
            if self.value < 1 or self.value > 30:
                raise ValueError("value have to between 1-30 mmol/L")
                
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e 
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting glucose record: {str(e)}")
            raise e
        
    def read(self):
        return {
            'id': self.id,
            'value': self.value,
            'time': self.time.isoformat(),
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
        
    def update(self, value=None, time=None, notes=None):
        try:
            if value is not None:
                value = float(value)
                if value < 1 or value > 30:
                    raise ValueError("Glucose value must be between 1 and 30 mmol/L")
                self.value = value
                self.status = self._get_status(value)
                
            if time is not None:
                self.time = time if isinstance(time, datetime) else datetime.fromisoformat(time)
                
            if notes is not None:
                self.notes = notes
                
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating glucose record: {str(e)}")
            return None

    @staticmethod
    def _get_status(value):
        if value < 4:
            return "Low"
        if value > 7.8:
            return "High"
        return "Normal"

    @staticmethod
    def restore(data):
        try:
            for item in data:
                existing_record = GlucoseRecord.query.filter_by(
                    value=item['value'],
                    time=datetime.fromisoformat(item['time']),
                    notes=item.get('notes', '')
                ).first()
                
                if not existing_record:
                    record = GlucoseRecord(
                        value=item['value'],
                        time=item['time'],
                        notes=item.get('notes', '')
                    )
                    db.session.add(record)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error restoring glucose records: {str(e)}")
            return False

def initGlucose():
    try:
        db.create_all()
        
        if not GlucoseRecord.query.first():
            from datetime import datetime, timedelta
            
            records = [
                GlucoseRecord(
                    value=5.2,
                    time=datetime.utcnow() - timedelta(days=2),
                    notes="Morning fasting"
                ),
                GlucoseRecord(
                    value=7.1,
                    time=datetime.utcnow() - timedelta(days=1, hours=2),
                    notes="After lunch"
                ),
                GlucoseRecord(
                    value=4.8,
                    time=datetime.utcnow() - timedelta(hours=3),
                    notes="Evening check"
                )
            ]
            
            for record in records:
                record.create()

        logging.info("GlucoseRecord table initialized and seeded successfully.")
    except Exception as e:
        logging.error(f"Error initializing GlucoseRecord table: {e}")
        raise e