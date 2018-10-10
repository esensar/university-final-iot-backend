# App initialization
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flasgger import Swagger
from flask_cors import CORS
from .tasks import celery_configurator

app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
swagger = Swagger(app, template_file='swagger/template.yaml')
swagger.template['info']['version'] = app.config['APP_VERSION']
CORS(app)
celery = celery_configurator.make_celery(app)


def setup_blueprints(app):
    """
    Sets up all of the blueprints for application

    All blueprints should be imported in this method and then added

    API blueprint should expose all resources, while other
    blueprints expose other domain specific functionalities
    They are exposed as blueprints just for consistency, otherwise
    they are just simple python packages/modules
    """
    from .accounts.blueprint import accounts_bp
    from .devices.blueprint import devices_bp
    from .dashboards.blueprint import dashboard_bp
    from .api.blueprint import api_bp
    from .mqtt.blueprint import mqtt_bp

    app.register_blueprint(accounts_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(mqtt_bp)
    app.register_blueprint(api_bp, url_prefix='/api')


setup_blueprints(app)


@app.route("/")
def root():
    return "Hello World!"
