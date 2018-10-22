import os

# App configuration
DEBUG = os.environ['DEBUG']
APP_VERSION = '0.2.2'

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "?['Z(Z\x83Y \x06T\x12\x96<\xff\x12\xe0\x1b\xd1J\xe0\xd9ld"
SECURITY_PASSWORD_SALT = "IyoZvOJb4feT3xKlYXyOJveHSIY4GDg6"

# MQTT configuration
MQTT_CLIENT_ID = 'final-iot-backend-server-' + os.environ['MQTT_CLIENT']
MQTT_BROKER_URL = 'broker.hivemq.com'
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = 'user'
MQTT_PASSWORD = 'secret'
MQTT_REFRESH_TIME = 1.0  # refresh time in seconds

# Celery config
CELERY_BROKER_URL = os.environ['REDIS_URL']
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']

# Mailer config
SMTP_LOGIN = os.environ['MAILGUN_SMTP_LOGIN']
SMTP_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
MAIL_SERVER = os.environ['MAILGUN_SMTP_SERVER']
MAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_DEBUG = False

# gmail authentication
MAIL_USERNAME = os.environ['MAILGUN_SMTP_LOGIN']
MAIL_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = 'final.iot.backend.mailer@gmail.com'

# Flasgger config
SWAGGER = {
    'uiversion': 3
}
