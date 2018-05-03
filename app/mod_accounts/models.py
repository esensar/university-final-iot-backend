from sqlalchemy import Column, Integer, String, ForeignKey, relationship
from app import db


class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    emails = Column(String, index=True, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", foreign_keys=[role_id])

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

    id = Column(Integer, primary_key=True)
    display_name = Column(String)

    def __init__(self, name):
        self.display_name = str(name)

    def __repr__(self):
        return '<Role %s>' % self.name
