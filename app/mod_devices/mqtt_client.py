import sys
import json
from flask_mqtt import Mqtt
from .models import Recording
from app import db, app

class MqttClient:
    def __init__(self):
        self.mqtt = Mqtt()
        self.initialized = False


    # Mqtt setup
    def setup(self, app):
        if not self.initialized:
            self.mqtt.init_app(app)
            self.mqtt.client.on_message = self.handle_mqtt_message
            self.mqtt.client.on_subscribe = self.handle_subscribe
            initialized = True

            @self.mqtt.on_connect()
            def handle_connect(client, userdata, flags, rc):
                print('MQTT client connected')
                self.mqtt.subscribe('device/+')

            @self.mqtt.on_disconnect()
            def handle_disconnect():
                print('MQTT client disconnected')

            print('MQTT client initialized')


    def tear_down(self):
        self.mqtt.unsubscribe_all()
        if hasattr(self.mqtt, 'client') and self.mqtt.client is not None:
            self.mqtt.client.disconnect()
        print('MQTT client destroyed')


    def handle_subscribe(self, client, userdata, mid, granted_qos):
        print('MQTT client subscribed')


    def handle_mqtt_message(self, client, userdata, message):
        print("Received message!")
        print("Topic: " + message.topic)
        print("Payload: " + message.payload.decode())
        try:
            # If type is JSON
            recording = self.parse_json_message(message.topic, message.payload.decode())
            with app.app_context():
                recording.save()
        except ValueError:
            print("ERROR!")
            error_type, error_instance, traceback = sys.exc_info()
            print("Type: " + str(error_type))
            print("Instance: " + str(error_instance))
            return


    def parse_json_message(self, topic, payload) -> Recording:
        try:
            json_msg = json.loads(payload)
            device_id = self.get_device_id(topic)
            return Recording(device_id=device_id,
                             record_type=json_msg["record_type"],
                             record_value=json_msg["record_value"],
                             recorded_at=json_msg["recorded_at"],
                             raw_json=json_msg)
        except KeyError:
            error_type, error_instance, traceback = sys.exc_info()
            raise ValueError("JSON parsing failed! Key error: "
                             + str(error_instance))


    def get_device_id(self, topic) -> int:
        device_token, device_id = topic.split("/")
        if device_token == "device":
            return int(device_id)
        else:
            raise ValueError("Topic is in invalid format")
