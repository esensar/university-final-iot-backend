import atexit
from flask import Blueprint
from .mqtt_client import MqttClient
from .models import Device, Recording

devices_bp = Blueprint('devices', __name__)


# When app dies, stop mqtt connection
def on_stop():
    MqttClient.tear_down()


atexit.register(on_stop)


# Setup
@devices_bp.record
def __on_blueprint_setup(setup_state):
    print('Blueprint setup')
    MqttClient.setup(setup_state.app)


# Public interface
def create_device(name, device_type=1):
    """
    Tries to create device with given parameters

    :param name: Desired device name
    :param device_type: Id of desired device type.
    By default it is 1 (STANDARD)
    :type name: string
    :type device_type: int
    :returns: True if device is successfully created
    :rtype: Boolean
    """
    device = Device(name, None, device_type)
    device.save()


def get_device_recordings(device_id):
    """
    Tries to get device recording for device with given parameters. Raises
    error on failure

    :param device_id: Id of device
    :type device_id: int
    :returns: List of Recordings for given device
    :rtype: List of Recording
    :raises: ValueError if device does not exist
    """
    if not Device.exists(id=device_id):
        raise ValueError("Device with id %s does not exist" % device_id)

    return Recording.get_many(device_id=device_id)


def get_device(device_id):
    """
    Tries to get device with given parameters. Raises error on failure

    :param device_id: Id of device
    :type device_id: int
    :returns: Requested device
    :rtype: Device
    :raises: ValueError if device does not exist
    """
    if not Device.exists(id=device_id):
        raise ValueError("Device with id %s does not exist" % device_id)

    return Device.get(id=device_id)
