import atexit
from flask import Flask
from app.mod_devices import setup_mqtt, tear_down_mqtt

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

def on_stop():
    print('Application stopping')
    tear_down_mqtt()

setup_mqtt(app)
atexit.register(on_stop)

@app.route("/")
def hello():
    return "Hello World!"
