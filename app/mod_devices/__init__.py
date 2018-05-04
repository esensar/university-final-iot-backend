import atexit
from flask import Blueprint
from .mqtt_client import MqttClient

devices = Blueprint('devices', __name__)
mqtt_client = None


# When app dies, stop mqtt connection
def on_stop():
    if mqtt_client:
        mqtt_client.tear_down()


atexit.register(on_stop)


# Routes
@devices.route("/")
def hello():
    return "Hello from devices!"


@devices.record
def on_blueprint_setup(setup_state):
    print('Blueprint setup')
    mqtt_client = MqttClient()

    if mqtt_client:
        mqtt_client.setup(setup_state.app)
