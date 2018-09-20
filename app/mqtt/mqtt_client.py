import sys
import json
from flask_mqtt import Mqtt
import app.devices as devices


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
            MqttClient.mqtt.client.on_publish = MqttClient.handle_publish
            MqttClient.__initialized = True

            @MqttClient.mqtt.on_connect()
            def handle_connect(client, userdata, flags, rc):
                print('MQTT client connected')
                MqttClient.mqtt.subscribe('device/+')

            @MqttClient.mqtt.on_disconnect()
            def handle_disconnect():
                print('MQTT client disconnected')

            @MqttClient.mqtt.on_log()
            def handle_logging(client, userdata, level, buf):
                print(level, buf)

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
            devices.create_recording(
                    MqttClient.get_device_id(message.topic),
                    json.loads(message.payload.decode()))
        except Exception:
            print("ERROR!")
            error_type, error_instance, traceback = sys.exc_info()
            print("Type: " + str(error_type))
            print("Instance: " + str(error_instance))
            return

    @staticmethod
    def handle_publish(client, userdata, mid):
        print("Published message! (" + str(mid) + ")")

    @staticmethod
    def get_device_id(topic):
        device_token, device_id = topic.split("/")
        if device_token == "device":
            return int(device_id)
        else:
            raise ValueError("Topic is in invalid format")
