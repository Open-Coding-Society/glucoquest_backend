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
        """
        初始化血糖记录
        :param value: 血糖值 (mmol/L)
        :param time: 测量时间
        :param notes: 备注信息
        :param _skip_status: 内部使用，跳过自动状态计算
        """
        self.value = float(value)
        self.time = time if isinstance(time, datetime) else datetime.fromisoformat(time)
        self.notes = notes or ""
        
        # 只有当不跳过时才自动计算状态
        if not _skip_status:
            self.status = self._calculate_status(self.value)

    @staticmethod
    def _calculate_status(value):
        """内部状态计算方法"""
        value = float(value)
        if value < 4: return "Low"
        if value > 7.8: return "High"
        return "Normal"

    def create(self):
        """创建记录方法（可选保留）"""
        try:
            if self.value < 1 or self.value > 30:
                raise ValueError("血糖值必须在1-30 mmol/L之间")
                
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e  # 抛出异常由上层处理
        
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