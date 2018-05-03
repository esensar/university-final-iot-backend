from datetime import datetime
from sqlalchemy import Model, DateTime, String, Column, Integer
from sqlalchemy.dialects.postgresql import JSON


class Recording(Model):
    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True)
    recorded_at = Column(DateTime, index=True,
                         default=datetime.utcnow())
    received_at = Column(DateTime, index=True,
                         default=datetime.utcnow())
    device_id = Column(Integer)
    record_type = Column(Integer, nullable=False)
    record_value = Column(String, nullable=False)
    raw_record = Column(JSON, nullable=True)

    def __init__(self, device_id, record_type,
                 record_value, recorded_at, raw_json):
        self.device_id = int(device_id)
        self.record_type = int(record_type)
        self.record_value = str(record_value)
        self.recorded_at = datetime.fromtimestamp(int(recorded_at))
        self.received_at = datetime.utcnow()
        self.raw_record = raw_json

    def __repr__(self):
        return '<Recording (value=%s, recorded_at=%s)>' % (
            self.record_value, self.recorded_at)
