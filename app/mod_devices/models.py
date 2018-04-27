from datetime import datetime
from . import db
from sqlalchemy.dialects.postgresql import JSON


class Recording(db.Model):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    recorded_at = db.Column(db.DateTime, index=True,
                            default=datetime.utcnow())
    received_at = db.Column(db.DateTime, index=True,
                            default=datetime.utcnow())
    device_id = db.Column(db.Integer)
    record_type = db.Column(db.Integer, nullable=False)
    record_value = db.Column(db.String, nullable=False)
    raw_record = db.Column(JSON, nullable=True)

    def __init__(self, device_id, record_type,
                 record_value, recorded_at, raw_json):
        self.device_id = device_id
        self.record_type = record_type
        self.record_value = record_value
        self.recorded_at = recorded_at
        self.received_at = datetime.utcnow()
        self.raw_record = raw_json

    def __repr__(self):
        return '<Recording %r>' % self.recorded_at
