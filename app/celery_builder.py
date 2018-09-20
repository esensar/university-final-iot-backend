# App initialization
import sys
from flask import Flask
from .tasks import celery as celery_configurator

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)
app.config['MQTT_CLIENT_ID'] = 'final-iot-backend-server-worker'
celery = celery_configurator.make_celery(app)


@celery.task()
def send_config(device_id, config):
    from flask_mqtt import Mqtt, MQTT_ERR_SUCCESS
    mqtt = Mqtt(app)

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        print('MQTT worker client connected')
        print("Sending configuration to device: " + str(device_id))
        print("Configuration: " + str(config))
        topic = 'device/' + str(device_id) + '/config'
        print("Targeting topic: " + topic)
        try:
            (result, mid) = mqtt.publish(topic, config, 2)
            if (result == MQTT_ERR_SUCCESS):
                print("Success!!!")
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
