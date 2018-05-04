import jwt
import datetime
from app import db, app


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", foreign_keys=[role_id])

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
        Stores current user to database
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
        return Account.query.all()

    @staticmethod
    def get(**kwargs):
        return Account.query.filter_by(**kwargs).first()

    def create_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
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
        except Exception as e:
            return e

    def __repr__(self):
        return '<Account (name=%s, role=%s)>' % self.username, self.role


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String)

    def __init__(self, name):
        self.display_name = str(name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Role.query.all()

    @staticmethod
    def get(roleId):
        return Role.query.filter_by(id=roleId)

    def __repr__(self):
        return '<Role %s>' % self.name
