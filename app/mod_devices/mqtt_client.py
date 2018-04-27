from datetime import datetime
from flask_mqtt import Mqtt
from .models import Recording
from . import db

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
    mqtt.subscribe('topic/state')


@mqtt.on_disconnect()
def handle_disconnect():
    print('MQTT client disconnected')


def handle_subscribe(client, userdata, mid, granted_qos):
    print('MQTT client subscribed')


def handle_mqtt_message(client, userdata, message):
    recording = Recording(1, 1, "315", datetime.utcnow(), "{}")
    db.session.add(recording)
    db.session.commit()
    print(message.payload.decode())
