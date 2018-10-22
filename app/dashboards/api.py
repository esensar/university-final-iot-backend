from .models import Dashboard


# Public interface
def create_dashboard(dashboard_data, name, account_id):
    """
    Tries to create dashboard with given parameters

    :param dashboard_data: JSON dashboard data
    :param account_id: Id of owner of this dashboard
    :param name: Name of the dashboard
    :type name: JSON
    :type account_id: int
    :type name: string
    :returns: True if dashboard is successfully created
    :rtype: Boolean
    """
    dashboard = Dashboard(account_id, dashboard_data, name)
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


def patch_dashboard(account_id, dashboard_id,
                    dashboard_data=None, active=None, name=None):
    """
    Tries to update dashboard with given parameters

    :param dashboard_data: JSON dashboard data
    :param dashboard_id: Id of the dashboard
    :type name: JSON
    :type dashboard_id: int
    """
    dashboard = Dashboard.get(id=dashboard_id)
    if dashboard_data is not None:
        dashboard.dashboard_data = dashboard_data
    if name is not None:
        dashboard.name = name
    dashboard.save()
    if active:
        set_active_dashboard(account_id, dashboard_id)


def delete_dashboard(dashboard_id):
    """
    Tries to delete dashboard with given id

    :param dashboard_id: Id of requested dashboard
    :type name: int
    """
    dashboard = Dashboard.get(id=dashboard_id)
    dashboard.delete()


def set_active_dashboard(account_id, dashboard_id):
    """
    Tries to set given dashboard as active

    :param dashboard_id: Id of requested dashboard
    :type name: int
    :param dashboard_id: Id of owner account
    :type name: int
    """
    Dashboard.deactivate_all_for_user(account_id)
    dashboard = Dashboard.get(id=dashboard_id)
    dashboard.active = True
    dashboard.save()


def get_active_dashboard(account_id):
    """
    Tries to fetch active dashboard owned by account with given id

    :param account_id: Id of owner account
    :type name: int
    :returns: active Dashboard object
    :rtype: Dashboard
    """
    return Dashboard.get(account_id=account_id, active=True)


def get_dashboards(account_id, active):
    """
    Tries to fetch dashboards owned by account with given id

    :param account_id: Id of owner account
    :type name: int
    :param active: Whether to filter active only
    :type name: bool
    :returns: Dashboard list
    :rtype: List of Dashboard
    """
    return Dashboard.get_many_filtered(account_id=account_id, active=active)
