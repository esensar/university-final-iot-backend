from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.mod_devices import setup_mqtt, tear_down_mqtt, devices

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
app.register_blueprint(devices, url_prefix='/devices')


@app.route("/")
def hello():
    return "Hello World!"
