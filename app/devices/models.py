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
        """
        Stores this recording to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Recording.query.all()

    @staticmethod
    def get_many(**kwargs):
        """
        Get many recording with given filters as a list

        Available filters:
         * id
         * device_id
         * record_type
         * recorded_at
         * received_at
         * record_value (probably useless)
         * raw_record (useless)

        """
        return Recording.query.filter_by(**kwargs).all()

    @staticmethod
    def get(**kwargs):
        """
        Get recordings with given filters

        Available filters:
         * id
         * device_id
         * record_type
         * recorded_at
         * received_at
         * record_value (probably useless)
         * raw_record (useless)

        """
        return Recording.query.filter_by(**kwargs).first()

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
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'))
    device_type = db.relationship("DeviceType", foreign_keys=[device_type_id])
    configuration = db.Column(JSON, nullable=True)

    def __init__(self, name, configuration=None, device_type=1):
        self.name = name
        self.configuration = configuration
        self.device_type_id = device_type

    def save(self):
        """
        Stores this device to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_many(**kwargs):
        """
        Get many devices with given filters as a list

        Available filters:
         * id
         * name
         * device_type_id
         * created_at
         * modified_at
         * configuration (useless)

        """
        return Device.query.filter_by(**kwargs).all()

    @staticmethod
    def get(**kwargs):
        """
        Get device with given filters

        Available filters:
         * id
         * name
         * device_type_id
         * created_at
         * modified_at
         * configuration (useless)

        """
        return Device.query.filter_by(**kwargs).first()

    def __repr__(self):
        return '<Device (name=%s, type=%s)>' % (
            self.name, self.device_type_id)


class DeviceType(db.Model):
    __tablename__ = 'device_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<DeviceType (name %s)>' % self.name
