from . import db


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", foreign_keys=[role_id])

    def __init__(self, username, password, role):
        self.username = str(username)
        self.password = str(password)
        if isinstance(role, Role):
            self.role_id = role.id
        else:
            self.role_id = int(role)

    def __repr__(self):
        return '<Account (name=%s, role=%s)>' % self.username, self.role


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String)

    def __init__(self, name):
        self.display_name = str(name)

    def __repr__(self):
        return '<Role %s>' % self.name
