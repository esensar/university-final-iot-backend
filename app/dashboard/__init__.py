from flask import Blueprint
from .models import Dashboard

dashboard_bp = Blueprint('dashboard', __name__)


# Public interface
def create_dashboard(dashboard_data, account_id):
    """
    Tries to create dashboard with given parameters

    :param dashboard_data: JSON dashboard data
    :param account_id: Id of owner of this dashboard
    :type name: JSON
    :type account_id: int
    :returns: True if dashboard is successfully created
    :rtype: Boolean
    """
    dashboard = Dashboard(account_id, dashboard_data)
    dashboard.save()


def get_dashboard(dashboard_id):
    """
    Tries to fetch dashboard with given id

    :param dashboard_id: Id of requested dashboard
    :type name: int
    :returns: Dashboard object
    :rtype: Dashboard
    """
    return Dashboard.get(id=dashboard_id)


def update_dashboard(dashboard_id, dashboard_data):
    """
    Tries to update dashboard with given parameters

    :param dashboard_data: JSON dashboard data
    :param dashboard_id: Id of the dashboard
    :type name: JSON
    :type dashboard_id: int
    """
    dashboard = Dashboard.get(id=dashboard_id)
    dashboard.dashboard_data = dashboard_data
    dashboard.save()


def get_dashboards(account_id):
    """
    Tries to fetch dashboards owned by account with given id

    :param account_id: Id of owner account
    :type name: int
    :returns: Dashboard list
    :rtype: List of Dashboard
    """
    return Dashboard.get_many(account_id=account_id)
