from .models import Dashboard, DashboardWidget


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
    return dashboard


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
        dashboard.active = True
    return dashboard


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


def create_widget(dashboard_id, device_id, height, width, x, y,
                  chart_type, filters):
    """
    Tries to create a dashboard widget
    """
    widget = DashboardWidget(dashboard_id, device_id, height, width, x, y,
                             chart_type, filters)
    widget.save()
    return widget


def delete_widget(widget_id):
    """
    Tries to delete widget with given id

    :param widget_id: Id of requested widget
    :type name: int
    """
    widget = DashboardWidget.get(id=widget_id)
    widget.delete()


def get_widgets(dashboard_id):
    """
    Tries to fetch widgets of a dashboard with dashboard_id

    :param dashboard_id: Id of owner dashboard
    :type name: int
    :returns: Widget list
    :rtype: List of Widgets
    """
    return DashboardWidget.get_many_for_dashboard(dashboard_id)


def get_widget(widget_id):
    """
    Tries to fetch widget with given id

    :param widget_id: Id of requested dashboard
    :type name: int
    :returns: Widget object
    :rtype: Widget
    """
    return DashboardWidget.get(id=widget_id)


def patch_widget(widget_id, device_id=None, height=None, width=None,
                 x=None, y=None, chart_type=None, filters=None):
    """
    Tries to update widget with given parameters
    """
    widget = DashboardWidget.get(id=widget_id)

    if device_id is not None:
        widget.device_id = device_id

    if height is not None:
        widget.height = height

    if width is not None:
        widget.width = width

    if x is not None:
        widget.x = x

    if y is not None:
        widget.y = y

    if chart_type is not None:
        widget.chart_type = chart_type

    if filters is not None:
        widget.filters = filters

    widget.save()
    return widget
