from app.core import db
from sqlalchemy.dialects.postgresql import JSON


class Dashboard(db.Model):
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    dashboard_data = db.Column(JSON, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'),
                           primary_key=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    def __init__(self, account_id, dashboard_data):
        self.account_id = account_id
        self.dashboard_data = dashboard_data

    def save(self):
        """
        Stores this dashboard to database
        This may raise errors
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes this dashboard from database
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def exists_with_any_of(**kwargs):
        """
        Checks if dashboard with any of the given arguments exists
        """
        for key, value in kwargs.items():
            args = {key: value}
            if Dashboard.query.filter_by(**args).first():
                return True
        return False

    @staticmethod
    def exists(**kwargs):
        """
        Checks if dashboard with all of the given arguments exists
        """
        if Dashboard.query.filter_by(**kwargs).first():
            return True
        return False

    @staticmethod
    def get_all():
        """
        Get all stored dashboards
        """
        return Dashboard.query.all()

    @staticmethod
    def get_many(**kwargs):
        """
        Get dashboards with given filters

        Available filters:
         * id
         * account_id
        """
        return Dashboard.query.filter_by(**kwargs).all()

    @staticmethod
    def get_many_filtered(account_id, active):
        """
        Get many dashboard with given filters

        Available filters:
         * active
        """
        query = Dashboard.query.filter(Dashboard.account_id == account_id)
        if active is not None:
            query = query.filter(Dashboard.active == active)
        return query.all()

    @staticmethod
    def deactivate_all_for_user(account_id):
        """
        Deactivates all dashboards for this user
        """
        db.session.query(Dashboard).filter(account_id == account_id) \
                                   .update({'active': False})
        db.session.commit()

    @staticmethod
    def get(**kwargs):
        """
        Get dashboard with given filters

        Available filters:
         * id
         * account_id
        """
        return Dashboard.query.filter_by(**kwargs).first_or_404()

    def __repr__(self):
        return '<Dashboard (dashboard_data=%s, account_id=%s)>' % (
                self.dashboard_data, self.account_id)
