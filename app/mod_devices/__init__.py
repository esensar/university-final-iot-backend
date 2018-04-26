import atexit
from flask import Blueprint
from flask_mqtt import Mqtt

devices = Blueprint('devices', __name__)
mqtt = Mqtt()

def on_stop():
    tear_down_mqtt()

atexit.register(on_stop)

@devices.route("/")
def hello():
    return "Hello from devices!"


@devices.record
def setup_mqtt(setup_state):
    mqtt.init_app(setup_state.app)
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
    mqtt.subscribe('topic/state')


@mqtt.on_disconnect()
def handle_disconnect():
    print('MQTT client disconnected')


def handle_subscribe(client, userdata, mid, granted_qos):
    print('MQTT client subscribed')


def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(message.payload.decode())
