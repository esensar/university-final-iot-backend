# App initialization
from flask import Flask
from .tasks.celery_configurator import make_celery

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)
app.config['MQTT_CLIENT_ID'] = app.config['MQTT_CLIENT_ID'] + '-worker'
task_builder = make_celery(app)
task_builder.autodiscover_tasks(['app.devices'])
