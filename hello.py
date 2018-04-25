from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
mqtt = Mqtt(app)

@app.route("/")
def hello():
    return "Hello World!"

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('topic/state')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(message.payload.decode())
