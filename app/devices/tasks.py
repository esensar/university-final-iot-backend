import sys
from app.celery_builder import task_builder
from flask import current_app as app


def connect_and_send_mqtt_message(topic, message):
    from flask_mqtt import Mqtt, MQTT_ERR_SUCCESS
    mqtt = Mqtt(app)

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        print('MQTT worker client connected')
        print("Targeting topic: " + topic)
        print("Sending message: " + message)
        try:
            (result, mid) = mqtt.publish(topic, message, 2)
            if (result == MQTT_ERR_SUCCESS):
                print("Successfully sent a message")
            print("Result: " + str(result))
            print("Message id: " + str(mid))
            mqtt.client.disconnect()
        except Exception:
            print("ERROR!")
            error_type, error_instance, traceback = sys.exc_info()
            print("Type: " + str(error_type))
            print("Instance: " + str(error_instance))
            mqtt.client.disconnect()
            return


@task_builder.task()
def send_config(device_id, config):
    print("Sending configuration to device: " + str(device_id))
    print("Configuration: " + str(config))
    topic = 'device/' + str(device_id) + '/config'
    connect_and_send_mqtt_message(topic, config)
