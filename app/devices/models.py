from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON


class Recording(db.Model):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    recorded_at = db.Column(db.DateTime, index=True,
                            default=db.func.current_timestamp())
    received_at = db.Column(db.DateTime, index=True,
                            default=db.func.current_timestamp())
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    record_type = db.Column(db.Integer, nullable=False)
    record_value = db.Column(db.String, nullable=False)
    raw_record = db.Column(JSON, nullable=True)

    def __init__(self, device_id, record_type,
                 record_value, recorded_at, raw_json):
        self.device_id = int(device_id)
        self.record_type = int(record_type)
        self.record_value = str(record_value)
        self.recorded_at = datetime.fromtimestamp(int(recorded_at))
        self.received_at = datetime.utcnow()
        self.raw_record = raw_json

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Recording.query.all()

    def __repr__(self):
        return '<Recording (value=%s, recorded_at=%s)>' % (
            self.record_value, self.recorded_at)


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    name = db.Column(db.String, nullable=False)
    device_type = db.Column(db.Integer, db.ForeignKey('device_types.id'))
    configuration = db.Column(JSON, nullable=True)


class DeviceType(db.Model):
    __tablename__ = 'device_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
