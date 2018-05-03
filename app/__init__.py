# App initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


def setup_blueprints(app):
    from .mod_devices import devices
    from .mod_accounts import accounts

    app.register_blueprint(devices, url_prefix='/devices')
    app.register_blueprint(accounts, url_prefix='/accounts')


setup_blueprints(app)


@app.route("/")
def hello():
    return "Hello World!"
