import sys
import hmac
import urllib.parse
import datetime
import hashlib
from secrets import token_urlsafe
from .models import (Device,
                     Recording,
                     DeviceAssociation,
                     DeviceType,
                     AccessLevel,
                     DeviceDocumentation)
from itsdangerous import URLSafeSerializer
from app.core import app
from app.errors import NotPresentError
from app.jsonql import api as jsonql


# Private helpers
def generate_hmac_for_message(device_id, raw_json):
    device = Device.get(id=device_id)
    raw_json_bytes = urllib.parse.urlencode(raw_json).encode('utf-8')
    return hmac.new(
            bytes(device.device_secret, 'utf-8'),
            raw_json_bytes,
            device.secret_algorithm).hexdigest()


def validate_hmac_in_message(device_id, raw_json):
    hmac_value = raw_json.pop('hmac', None)
    calculated_hmac = generate_hmac_for_message(device_id, raw_json)
    if not hmac.compare_digest(hmac_value, calculated_hmac):
        raise ValueError("Bad hmac")


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
    return device


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
    return device_type


def set_device_configuration(device_id, configuration_json):
    """
    Tries to update configuration of device with given id

    :param device_id: Id of device to change configuration
    :param configuration_json: New configuration
    :type device_id: int
    :type configuration_json: JSON
    :rtype: Boolean
    """
    from .tasks import send_config
    device = Device.get(id=device_id)
    device.configuration = configuration_json
    device.save()
    configuration_json['hmac'] = generate_hmac_for_message(
            device_id,
            configuration_json)
    send_config.delay(device_id, str(configuration_json))
    return device


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
        raise NotPresentError("Device with id %s does not exist" % device_id)

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
        raise NotPresentError("Device with id %s does not exist" % device_id)

    return Recording.get_many_filtered(device_id, record_type,
                                       start_date, end_date)


def get_latest_device_recording(device_id):
    """
    Tries to get most recent recording for device with given parameters. Raises
    error on failure

    :param device_id: Id of device
    :type device_id: int
    :returns: Single recording (last recording)
    :rtpe: Recording
    :raises: ValueError if device does not exist
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device with id %s does not exist" % device_id)

    return Recording.get_latest(device_id)


def get_device(device_id):
    """
    Tries to get device with given parameters. Raises error on failure

    :param device_id: Id of device
    :type device_id: int
    :returns: Requested device
    :rtype: Device
    """
    return Device.get(id=device_id)


def reset_device_secret(device_id):
    """
    Resets device secret for device with given parameters. Raises error on
    failure

    :param device_id: Id of device
    :type device_id: int
    :returns: Requested device
    :rtype: Device
    """
    device = Device.get(id=device_id)
    device.device_secret = token_urlsafe(32)
    device.save()
    return device


def update_algorithm(device_id, algorithm):
    """
    Updates device secret algorithm for device with given parameters. Raises
    error on failure

    :param device_id: Id of device
    :type device_id: int
    :param algorithm: Name of new algorithm
    :type algorithm: string
    :returns: Requested device
    :rtype: Device
    """
    if algorithm not in hashlib.algorithms_available:
        raise ValueError("Unsupported algorithm! Supported algorithms: " +
                         str(hashlib.algorithms_available) + ". Some of " +
                         "these may not work on all platforms. These are " +
                         "guaranteed to work on every platform: " +
                         str(hashlib.algorithms_guaranteed))
    device = Device.get(id=device_id)
    device.secret_algorithm = algorithm
    device.save()
    return device


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


def get_device_documentation(device_id):
    """
    Tries to get device documentation associated to given device.

    :returns: DeviceDocumentation
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device with id %s does not exist" % device_id)
    return DeviceDocumentation.get_for_device(device_id)


def update_device_documentation(device_id, new_text):
    """
    Tries to update device documentation
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device with id %s does not exist" % device_id)
    device_documentation = DeviceDocumentation.get_for_device(device_id)
    device_documentation.text = new_text
    device_documentation.save()
    return device_documentation


def get_device_types():
    """
    Tries to get all device types. Raises error on failure

    :returns: List of device types
    :rtype: List of DeviceTypes
    """
    return DeviceType.get_many()


def parse_raw_json_recording(device_id, json_msg):
    """
    Parses raw json recording and creates Recording object

    :param device_id: Id of device
    :type device_id: int
    :param raw_json: Raw json received
    :type raw_json: json
    :raises: ValueError if parsing fails
    """
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


def create_recording_and_return(device_id, raw_json,
                                authenticated=False):
    """
    Tries to create recording with given parameters and returns it.
    Raises error on failure

    :param device_id: Id of device
    :type device_id: int
    :param raw_json: Raw json received
    :type raw_json: json
    :raises: ValueError if parsing fails or device does not exist
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device does not exist!")

    if not authenticated:
        validate_hmac_in_message(device_id, raw_json)

    recording = parse_raw_json_recording(device_id, raw_json)
    recording.save()
    return recording


def create_recording(device_id, raw_json):
    """
    Tries to create recording with given parameters. Raises error on failure

    :param device_id: Id of device
    :type device_id: int
    :param raw_json: Raw json received
    :type raw_json: json
    :raises: ValueError if parsing fails or device does not exist
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device does not exist!")

    validate_hmac_in_message(device_id, raw_json)
    recording = parse_raw_json_recording(device_id, raw_json)
    with app.app_context():
        recording.save()


def create_targeted_device_sharing_token(
        device_id, access_level_id, account_id=None):
    """
    Creates device sharing token that can be passed only to account with passed
    id in order to allow access to device

    :param device_id: Id of device
    :type device_id: int
    :param access_level_id: Id of access level this link will give
    :type access_level_id: int
    :param account_id: Id of account
    :type account_id: int
    :raises: ValueError if device does not exist
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device does not exist!")
    if not AccessLevel.exists(id=access_level_id):
        raise NotPresentError("AccessLevel does not exist!")

    data_to_serialize = {
            'device_id': device_id,
            'access_level_id': access_level_id
    }

    if account_id is not None:
        data_to_serialize['account_id'] = account_id

    serializer = URLSafeSerializer(app.config['SECRET_KEY'],
                                   salt=app.config['SECURITY_PASSWORD_SALT'])
    token = serializer.dumps(data_to_serialize)
    return token


def activate_device_sharing_token(account_id, token):
    """
    Activates device sharing token for account with passed id

    :param account_id: Id of account
    :type account_id: int
    :param token: Token created by device owner
    :type token: string
    :raises: ValueError if device does not exist
    """
    serializer = URLSafeSerializer(app.config['SECRET_KEY'],
                                   salt=app.config['SECURITY_PASSWORD_SALT'])
    token_data = serializer.loads(token)
    device_id = token_data['device_id']
    access_level_id = token_data['access_level_id']
    if (token_data.get('account_id') or account_id) != account_id:
        return False

    if not Device.exists(id=device_id):
        raise NotPresentError("Device does not exist!")

    device_association = DeviceAssociation(device_id, account_id,
                                           access_level_id)
    device_association.save()
    return True


def run_custom_query(device_id, request):
    """
    Runs custom query as defined by jsonql module
    """
    if not Device.exists(id=device_id):
        raise NotPresentError("Device does not exist!")

    def recording_field_provider(name):
        if name == 'record_value':
            return Recording.record_value
        if name == 'record_type':
            return Recording.record_type
        if name == 'device_id':
            return Recording.device_id
        if name == 'recorded_at':
            return Recording.recorded_at
        if name == 'received_at':
            return Recording.received_at

    resulting_query = jsonql.run_query_on(Recording.query.with_entities(),
                                          recording_field_provider,
                                          **request)
    final_query = resulting_query.filter(Recording.device_id == device_id)
    resulting_columns = final_query.column_descriptions
    result = final_query.all()
    formatted_result = []
    for row in result:
        formatted_row = {}
        for idx, col in enumerate(row):
            if isinstance(col, datetime.datetime):
                col = col.replace(tzinfo=datetime.timezone.utc).isoformat()
            formatted_row[resulting_columns[idx]['name']] = col
        formatted_result.append(formatted_row)
    return formatted_result
