import sys
import json
from flask_mqtt import Mqtt
from .models import Recording

mqtt = Mqtt()


# Mqtt setup
def setup_mqtt(app):
    mqtt.init_app(app)
    mqtt.client.on_message = handle_mqtt_message
    mqtt.client.on_subscribe = handle_subscribe
    print('MQTT client initialized')


def tear_down_mqtt():
    mqtt.unsubscribe_all()
    if hasattr(mqtt, 'client') and mqtt.client is not None:
        mqtt.client.disconnect()
    print('MQTT client destroyed')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('MQTT client connected')
    mqtt.subscribe('device/+')


@mqtt.on_disconnect()
def handle_disconnect():
    print('MQTT client disconnected')


def handle_subscribe(client, userdata, mid, granted_qos):
    print('MQTT client subscribed')


def handle_mqtt_message(client, userdata, message):
    from .. import db
    print("Received message!")
    print("Topic: " + message.topic)
    print("Payload: " + message.payload.decode())
    try:
        # If type is JSON
        recording = parse_json_message(message.topic, message.payload.decode())
        db.session.add(recording)
        db.session.commit()
        print(recording)
    except ValueError:
        print("ERROR!")
        error_type, error_instance, traceback = sys.exc_info()
        print("Type: " + str(error_type))
        print("Instance: " + str(error_instance))
        return


def parse_json_message(topic, payload) -> Recording:
    try:
        json_msg = json.loads(payload)
        device_id = get_device_id(topic)
        return Recording(device_id, json_msg["record_type"],
                         json_msg["record_value"], json_msg["recorded_at"],
                         json_msg)
    except KeyError:
        error_type, error_instance, traceback = sys.exc_info()
        raise ValueError("JSON parsing failed! Key error: "
                         + str(error_instance))


def get_device_id(topic) -> int:
    device_token, device_id = topic.split("/")
    if device_token == "device":
        return int(device_id)
    else:
        raise ValueError("Topic is in invalid format")
