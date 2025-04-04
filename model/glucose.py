from __init__ import app, db
import logging
from datetime import datetime

class GlucoseRecord(db.Model):
    __tablename__ = 'glucose'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)  # 血糖值 (mmol/L)
    time = db.Column(db.DateTime, nullable=False)  # 测量时间
    notes = db.Column(db.String(500))  # 备注
    status = db.Column(db.String(10), nullable=False)  # 状态: Low/Normal/High
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 记录创建时间
    
    def __init__(self, value, time, notes=None):
        """
        初始化血糖记录
        :param value: 血糖值 (mmol/L)
        :param time: 测量时间 (datetime或ISO格式字符串)
        :param notes: 备注信息 (可选)
        """
        self.value = float(value)
        self.time = time if isinstance(time, datetime) else datetime.fromisoformat(time)
        self.notes = notes or ""
        self.status = self._get_status(self.value)

    def create(self):
        """创建新的血糖记录"""
        try:
            # 验证血糖值范围
            if self.value < 1 or self.value > 30:
                raise ValueError("Glucose value must be between 1 and 30 mmol/L")
                
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating glucose record: {str(e)}")
            return None

    def delete(self):
        """删除血糖记录"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting glucose record: {str(e)}")
            raise e
        
    def read(self):
        """返回记录的字典表示"""
        return {
            'id': self.id,
            'value': self.value,
            'time': self.time.isoformat(),
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
        
    def update(self, value=None, time=None, notes=None):
        """更新血糖记录"""
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
        """根据血糖值确定状态"""
        if value < 4:
            return "Low"
        if value > 7.8:
            return "High"
        return "Normal"

    @staticmethod
    def restore(data):
        """从备份数据恢复血糖记录"""
        try:
            for item in data:
                # 检查记录是否已存在
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
    """初始化血糖记录表并添加示例数据"""
    try:
        db.create_all()
        
        if not GlucoseRecord.query.first():
            from datetime import datetime, timedelta
            
            # 创建一些示例数据
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