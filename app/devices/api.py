import sys
from .models import Device, Recording, DeviceAssociation, DeviceType
from app.core import app


# Public interface
def create_device(name, account_id, device_type=1):
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
    device_association = DeviceAssociation(device.id, account_id)
    device_association.save()


def create_device_type(name):
    """
    Tries to create device type with given parameters

    :param name: Desired device type name
    :type name: string
    :returns: True if device type is successfully created
    :rtype: Boolean
    """
    device_type = DeviceType(name)
    device_type.save()


def set_device_configuration(device_id, configuration_json):
    """
    Tries to update configuration of device with given id

    :param device_id: Id of device to change configuration
    :param configuration_json: New configuration
    :type device_id: int
    :type configuration_json: JSON
    :rtype: Boolean
    """
    from app.celery_builder import send_config
    device = Device.get(id=device_id)
    device.configuration = configuration_json
    device.save()
    send_config.delay(device_id, str(configuration_json))


def get_device_configuration(device_id):
    """
    Tries to get configuration for device with given parameters.

    :param device_id: Id of device
    :type device_id: int
    :returns: Configuration of given device
    :rtype: JSON Configuration
    """
    return Device.get(id=device_id).configuration


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


def get_device_recordings_filtered(device_id, record_type=None,
                                   start_date=None, end_date=None):
    """
    Tries to get device recording for device with given parameters. Raises
    error on failure

    :param device_id: Id of device
    :param record_type: Type of recording
    :param start_date: Lower date limit
    :param end_date: Upper date limit
    :type device_id: int
    :type record_type: int
    :type start_date: Date (string: %d-%m-%Y)
    :type end_date: Date (string: %d-%m-%Y)
    :returns: List of Recordings for given filters
    :rtype: List of Recording
    :raises: ValueError if device does not exist
    """
    if not Device.exists(id=device_id):
        raise ValueError("Device with id %s does not exist" % device_id)

    return Recording.get_many_filtered(device_id, record_type,
                                       start_date, end_date)


def get_device(device_id):
    """
    Tries to get device with given parameters. Raises error on failure

    :param device_id: Id of device
    :type device_id: int
    :returns: Requested device
    :rtype: Device
    """
    return Device.get(id=device_id)


def can_user_access_device(account_id, device_id):
    """
    Checks if user with given account_id can access device with given device_id

    :param account_id: Id of account
    :param device_id: Id of device
    :type account_id: int
    :type device_id: int
    :returns: true if device is accessible by this account, false otherwise
    :rtype: Boolean
    """
    return len(DeviceAssociation.get_many(account_id=account_id,
                                          device_id=device_id)) > 0


def get_device_type(device_type_id):
    """
    Tries to get device type with given parameters. Raises error on failure

    :param device_type_id: Id of device type
    :type device_type_id: int
    :returns: Requested device type
    :rtype: DeviceType
    """
    return DeviceType.get(id=device_type_id)


def delete_device(device_id):
    """
    Tries to delete device with given parameters. Does not raise errors
    """
    Device.get(id=device_id).delete()


def get_devices(account_id):
    """
    Tries to get all devices associated to account. Raises error on
    failure

    :returns: List of Devices associated to this account
    :rtype: List of Devices
    """
    return Device.get_many_for_user(account_id)


def get_device_types():
    """
    Tries to get all device types. Raises error on failure

    :returns: List of device types
    :rtype: List of DeviceTypes
    """
    return DeviceType.get_many()


def create_recording(device_id, raw_json):
    """
    Tries to create recording with given parameters. Raises error on failure

    :param device_id: Id of device
    :type device_id: int
    :param raw_json: Raw json received
    :type raw_json: json
    :raises: ValueError if parsing fails or device does not exist
    """
    def parse_raw_json_recording(device_id, json_msg):
        try:
            return Recording(device_id=device_id,
                             record_type=json_msg["record_type"],
                             record_value=json_msg["record_value"],
                             recorded_at=json_msg["recorded_at"],
                             raw_json=json_msg)
        except KeyError:
            error_type, error_instance, traceback = sys.exc_info()
            raise ValueError("JSON parsing failed! Key error: "
                             + str(error_instance))

    if not Device.exists(id=device_id):
        raise ValueError("Device does not exist!")

    recording = parse_raw_json_recording(device_id, raw_json)
    with app.app_context():
        recording.save()
