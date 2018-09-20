# App initialization
from flask import Flask
from .tasks import celery as celery_configurator

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)
app.config['MQTT_CLIENT_ID'] = 'final-iot-backend-server-worker'
celery = celery_configurator.make_celery(app)
