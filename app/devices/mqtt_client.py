import sys
import json
from flask_mqtt import Mqtt
from .models import Recording
from app import app


class MqttClient:
    __initialized = False
    mqtt = Mqtt()

    # Mqtt setup
    @staticmethod
    def setup(app):
        if not MqttClient.__initialized:
            MqttClient.mqtt.init_app(app)
            MqttClient.mqtt.client.on_message = MqttClient.handle_mqtt_message
            MqttClient.mqtt.client.on_subscribe = MqttClient.handle_subscribe
            MqttClient.__initialized = True

            @MqttClient.mqtt.on_connect()
            def handle_connect(client, userdata, flags, rc):
                print('MQTT client connected')
                MqttClient.mqtt.subscribe('device/+')

            @MqttClient.mqtt.on_disconnect()
            def handle_disconnect():
                print('MQTT client disconnected')

            print('MQTT client initialized')

    @staticmethod
    def tear_down():
        if MqttClient.__initialized:
            MqttClient.mqtt.unsubscribe_all()
            if (hasattr(MqttClient.mqtt, 'client') and
                    MqttClient.mqtt.client is not None):
                MqttClient.mqtt.client.disconnect()
            print('MQTT client destroyed')

    @staticmethod
    def handle_subscribe(client, userdata, mid, granted_qos):
        print('MQTT client subscribed')

    @staticmethod
    def handle_mqtt_message(client, userdata, message):
        print("Received message!")
        print("Topic: " + message.topic)
        print("Payload: " + message.payload.decode())
        try:
            # If type is JSON
            recording = MqttClient.parse_json_message(
                    message.topic, message.payload.decode())
            with app.app_context():
                recording.save()
        except ValueError:
            print("ERROR!")
            error_type, error_instance, traceback = sys.exc_info()
            print("Type: " + str(error_type))
            print("Instance: " + str(error_instance))
            return

    @staticmethod
    def parse_json_message(topic, payload) -> Recording:
        try:
            json_msg = json.loads(payload)
            device_id = MqttClient.get_device_id(topic)
            return Recording(device_id=device_id,
                             record_type=json_msg["record_type"],
                             record_value=json_msg["record_value"],
                             recorded_at=json_msg["recorded_at"],
                             raw_json=json_msg)
        except KeyError:
            error_type, error_instance, traceback = sys.exc_info()
            raise ValueError("JSON parsing failed! Key error: "
                             + str(error_instance))

    @staticmethod
    def get_device_id(topic) -> int:
        device_token, device_id = topic.split("/")
        if device_token == "device":
            return int(device_id)
        else:
            raise ValueError("Topic is in invalid format")
