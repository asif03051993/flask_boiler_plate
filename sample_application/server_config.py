# Statement for enabling the development environment
DEBUG = True

# environment
TYPE = 'LOCAL'

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'postgres://localhost/sampledb'
SQLALCHEMY_POOL_SIZE = 20

# Enable for sql alchemy logs
# SQLALCHEMY_ECHO=True

# Disbaling Flask-SQLAlchemy's own event notification system (otherwise causes little overhead i.e extra memory).
# Instead use sql alchemy's event system.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Cache config
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_KEY_PREFIX = 'sample-application'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0

# StatsD Config
STATSD_HOST = '127.0.0.1'
# application_environment
STATSD_PREFIX = 'sample_application_local'

# Celery Config
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'