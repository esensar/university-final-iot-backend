import time
from datetime import datetime
import datetime as datetime_module
from app.core import db
from sqlalchemy.dialects.postgresql import JSON
from secrets import token_urlsafe


class Recording(db.Model):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recorded_at = db.Column(db.DateTime, index=True,
                            default=db.func.current_timestamp())
    received_at = db.Column(db.DateTime, index=True,
                            default=db.func.current_timestamp())
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    record_type = db.Column(db.Integer, nullable=False)
    record_value = db.Column(db.Float, nullable=False)
    raw_record = db.Column(JSON, nullable=True)

    def __init__(self, device_id, record_type,
                 record_value, recorded_at, raw_json):
        self.device_id = int(device_id)
        self.record_type = int(record_type)
        self.record_value = float(record_value)
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

    def delete(self):
        """
        Deletes this recording from database
        """
        db.session.delete(self)
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
    def get_many_filtered(device_id, record_type, date_start, date_end):
        """
        Get many recording with given filters as a list

        Available filters:
         * record_type
         * recorded_at (upper and lower limit)
        """
        query = Recording.query.filter(Recording.device_id == device_id)
        if record_type is not None:
            query = query.filter(Recording.record_type == record_type)
        if date_start is not None:
            lower_limit = time.mktime(datetime.strptime(date_start,
                                      "%d-%m-%Y").timetuple())
            query = query.filter(Recording.recorded_at >
                                 db.func.to_timestamp(lower_limit))
        if date_end is not None:
            upper_limit = time.mktime(
                    (datetime.strptime(
                        date_end,
                        "%d-%m-%Y"
                        )+datetime_module.timedelta(days=1)).timetuple())
            query = query.filter(Recording.recorded_at <
                                 db.func.to_timestamp(upper_limit))
        return query.all()

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
        return Recording.query.filter_by(**kwargs).first_or_404()

    def __repr__(self):
        return '<Recording (value=%s, recorded_at=%s)>' % (
            self.record_value, self.recorded_at)


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    device_secret = db.Column(db.String, nullable=False)
    secret_algorithm = db.Column(db.String, nullable=False)
    configuration = db.Column(JSON, nullable=True)

    users = db.relationship("DeviceAssociation",
                            cascade="save-update, merge, delete")
    recordings = db.relationship("Recording",
                                 cascade="save-update, merge, delete")
    widgets = db.relationship("DashboardWidget",
                              cascade="save-update, merge, delete")
    documentations = db.relationship("DeviceDocumentation",
                                     cascade="save-update, merge, delete")

    def __init__(self, name, configuration=None, device_type=1):
        self.name = name
        self.configuration = configuration
        self.device_type_id = device_type
        self.secret_algorithm = 'sha256'
        self.device_secret = token_urlsafe(32)

    def save(self):
        """
        Stores this device to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes this recording from database
        """
        db.session.delete(self)
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
        return Device.query.filter_by(**kwargs).paginate(
                None, None, False).items

    @staticmethod
    def get_many_for_user(account_id):
        """
        Get many devices which are associated to account
        """
        return Device.query.filter(
                Device.users.any(account_id=account_id)
                ).paginate(None, None, False).items

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
        return Device.query.filter_by(**kwargs).first_or_404()

    @staticmethod
    def exists(**kwargs):
        """
        Checks if device with all of the given arguments exists
        """
        if Device.query.filter_by(**kwargs).first():
            return True
        return False

    def __repr__(self):
        return '<Device (name=%s, type=%s)>' % (
            self.name, self.device_type_id)


class DeviceAssociation(db.Model):
    __tablename__ = 'device_associations'

    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'),
                          primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'),
                           primary_key=True)
    access_level = db.Column(db.Integer, db.ForeignKey('access_levels.id'),
                             nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    access_level_data = db.relationship("AccessLevel",
                                        foreign_keys=[access_level])

    def __init__(self, device_id, account_id, access_level=1):
        self.device_id = device_id
        self.account_id = account_id
        self.access_level = access_level

    def save(self):
        """
        Stores this device association to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_many(**kwargs):
        """
        Get many device associations with given filters as a list

        Available filters:
         * device_id
         * account_id
        """
        return DeviceAssociation.query.filter_by(**kwargs).all()

    @staticmethod
    def get_for_user(account_id):
        """
        Get many device associations for user with account id passed in
        parameter
        """
        return DeviceAssociation.get_many(account_id=account_id)

    @staticmethod
    def get_for_device(device_id):
        """
        Get many device associations for device with account id passed in
        parameter
        """
        return DeviceAssociation.get_many(device_id=device_id)

    def __repr__(self):
        return '<DeviceAssociation (device_id=%s, accoount_id=%s)>' % (
                self.device_id, self.account_id)


class DeviceType(db.Model):
    __tablename__ = 'device_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    def save(self):
        """
        Stores this device type to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_many(**kwargs):
        """
        Get many devices types with given filters as a list

        Available filters:
         * id
         * name
        """
        return DeviceType.query.filter_by(**kwargs).paginate(
                None, None, False).items

    @staticmethod
    def get(**kwargs):
        """
        Get device type with given filters

        Available filters:
         * id
         * name
        """
        return DeviceType.query.filter_by(**kwargs).first_or_404()

    @staticmethod
    def exists(**kwargs):
        """
        Checks if device type with all of the given arguments exists
        """
        if DeviceType.query.filter_by(**kwargs).first():
            return True
        return False

    def __repr__(self):
        return '<DeviceType (name %s)>' % self.name


class DeviceDocumentation(db.Model):
    __tablename__ = 'device_documentations'

    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'),
                          primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    def __init__(self, device_id, text):
        self.device_id = device_id
        self.text = text

    def save(self):
        """
        Stores this device documentation to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(**kwargs):
        """
        Get device documentation with given filters

        Available filters:
         * device_id
        """
        return DeviceDocumentation.query.filter_by(**kwargs).first()

    @staticmethod
    def get_for_device(device_id):
        """
        Get documentation for device with device id passed in
        parameter
        """
        return (DeviceDocumentation.get(device_id=device_id) or
                DeviceDocumentation(device_id, ""))

    def __repr__(self):
        return '<DeviceDocumentation (device_id %s)>' % self.device_id

class AccessLevel(db.Model):
    __tablename__ = 'access_levels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    permissions = db.Column(db.ARRAY(db.String), nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    def __init__(self, name, permissions=['VIEW_DEVICE']):
        self.name = name
        self.permissions = permissions

    @staticmethod
    def exists(**kwargs):
        """
        Checks if access level with all of the given arguments exists
        """
        if AccessLevel.query.filter_by(**kwargs).first():
            return True
        return False

    def __repr__(self):
        return '<AccessLevel (name %s)>' % self.name
