import jwt
import datetime
from app.core import db, app
from calendar import timegm


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", foreign_keys=[role_id])
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    def __init__(self, username, password, email, role=2):
        self.username = str(username)
        self.password = str(password)
        self.email = str(email)
        if isinstance(role, Role):
            self.role_id = role.id
        else:
            self.role_id = int(role)

    def save(self):
        """
        Stores this user to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def exists_with_any_of(**kwargs):
        """
        Checks if user with any of the given arguments exists
        """
        for key, value in kwargs.items():
            args = {key: value}
            if Account.query.filter_by(**args).first():
                return True
        return False

    @staticmethod
    def exists(**kwargs):
        """
        Checks if user with all of the given arguments exists
        """
        if Account.query.filter_by(**kwargs).first():
            return True
        return False

    @staticmethod
    def get_all():
        """
        Get all stored accounts
        """
        return Account.query.all()

    @staticmethod
    def get(**kwargs):
        """
        Get account with given filters

        Available filters:
         * username
         * email
         * role_id
         * id
         * password (useless, but not forbidden)

        """
        return Account.query.filter_by(**kwargs).first()

    def create_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        current_time = datetime.datetime.utcnow()
        payload = {
            'exp': current_time + datetime.timedelta(days=0, hours=1),
            'iat': current_time,
            'sub': self.id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def validate_token(token):
        """
        Validates given Auth token
        :rtype: Account
        :return: Account associated with token
        """
        payload = jwt.decode(
            token,
            app.config.get('SECRET_KEY'),
            algorithms=['HS256']
        )
        current_time = timegm(datetime.datetime.utcnow().utctimetuple())
        if current_time > payload['exp']:
            raise ValueError("Expired token")
        return Account.get(id=payload['sub'])

    def __repr__(self):
        return '<Account (name=%s, role=%s)>' % (self.username, self.role)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String, unique=True)
    permissions = db.Column(db.ARRAY(db.String))

    def __init__(self, name, permissions):
        self.display_name = str(name)
        self.permissions = permissions

    def save(self):
        """
        Stores this role to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """
        Get all stored roles
        """
        return Role.query.all()

    @staticmethod
    def get(roleId):
        """
        Get role with id = roleId
        """
        return Role.query.filter_by(id=roleId).first_or_404()

    def __repr__(self):
        return '<Role %s (%s)>' % self.display_name, self.permissions
