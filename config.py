import os

# App configuration
DEBUG = False

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

# MQTT configuration
MQTT_BROKER_URL = 'broker.hivemq.com'
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = 'user'
MQTT_PASSWORD = 'secret'
MQTT_REFRESH_TIME = 1.0  # refresh time in seconds
