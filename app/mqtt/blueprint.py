import atexit
from flask import Blueprint
from .mqtt_client import MqttClient

mqtt_bp = Blueprint('mqtt', __name__)


# Setup
@mqtt_bp.record
def __on_blueprint_setup(setup_state):
    MqttClient.setup(setup_state.app)


# When app dies, stop mqtt connection
def on_stop():
    MqttClient.tear_down()


atexit.register(on_stop)
