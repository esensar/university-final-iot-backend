from app import db


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", foreign_keys=[role_id])

    def __init__(self, username, password, email, role):
        self.username = str(username)
        self.password = str(password)
        self.email = str(email)
        if isinstance(role, Role):
            self.role_id = role.id
        else:
            self.role_id = int(role)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Account.query.all()

    @staticmethod
    def get(accId):
        return Account.query.filter_by(id = accId)

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
        return Role.query.filter_by(id = accId)

    def __repr__(self):
        return '<Role %s>' % self.name
