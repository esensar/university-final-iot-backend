from datetime import datetime
from . import db
from sqlalchemy.dialects.postgresql import JSON

class Recording(db.Model):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    recorded_at = db.Column(db.DateTime, primary_key=True, index=True,
            default=datetime.utcnow())
    device_id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.Integer, nullable=False)
    record_value = db.Column(db.String, nullable=False)
    raw_record = db.Column(JSON, nullable=True)

    def __init__(self, device_id, record_type, record_value):
        self.device_id = device_id
        self.record_type = record_type
        self.record_value = record_value

    def __repr__(self):
        return '<Recording %r>' % self.recorded_at
