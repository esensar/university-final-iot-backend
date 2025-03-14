import os

# App configuration
DEBUG = os.environ['DEBUG']
APP_VERSION = '0.4.6'
APP_RELEASE_VERSION_STRING = (os.environ.get('HEROKU_RELEASE_VERSION')
                              or 'Unknown')

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
CSRF_SESSION_KEY = os.environ.get('CSRF_SECRET') or "secret"

# Secret key for signing cookies
SECRET_KEY = (os.environ.get('APP_SECRET_KEY') or
              "?['Z(Z\x83Y\x06T\x12\x96<\xff\x12\xe0\x1b\xd1J\xe0\xd9ld")
SECURITY_PASSWORD_SALT = (os.environ.get('APP_SECRETS_SALT') or
                          "IyoZvOJb4feT3xKlYXyOJveHSIY4GDg6")

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
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = False

# gmail authentication
MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = 'final.iot.backend.mailer@gmail.com'
MAIL_CONTACT_ACCOUNTS = ['esarajcic1@etf.unsa.ba', 'valjic1@etf.unsa.ba']

# frontend
FRONTEND_URL = (os.environ.get('IOT_FRONTEND_URL') or
                'http://iot-frontend-app.herokuapp.com/')

# Flasgger config
SWAGGER = {
    'uiversion': 3
}
