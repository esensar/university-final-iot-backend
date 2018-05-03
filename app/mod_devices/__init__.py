import atexit
from flask import Blueprint
from .mqtt_client import tear_down_mqtt, setup_mqtt

devices = Blueprint('devices', __name__)


# When app dies, stop mqtt connection
def on_stop():
    tear_down_mqtt()


atexit.register(on_stop)


# Routes
@devices.route("/")
def hello():
    return "Hello from devices!"


@devices.record
def on_blueprint_setup(setup_state):
    setup_mqtt(setup_state.app)
