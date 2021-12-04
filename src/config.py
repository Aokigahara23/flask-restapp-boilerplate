"""Application configuration."""
import os
import secrets
from datetime import timedelta


def get_host_uri():
    hostname = os.getenv('REST_DB_HOST')
    username = os.getenv('REST_DB_USER_NAME')
    password = os.getenv('REST_DB_PASSWORD')
    db_name = os.getenv('REST_DB_NAME')
    db_port = os.getenv('REST_DB_PORT') or 5432
    return f'{username}:{password}@{hostname}:{db_port}/{db_name}'


class Config(object):
    """Base configuration."""

    # FLASK_COMMON
    SECRET_KEY = os.environ.get('REST_KEY', secrets.token_urlsafe(20))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # BCRYPT CONFIG
    BCRYPT_LOG_ROUNDS = 13
    BCRYPT_HANDLE_LONG_PASSWORDS = True

    # SQLALCHEMY COMMON
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False

    # DB
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{get_host_uri()}'

    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 500
    CACHE_REDIS_HOST = 'redis-container'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_DB = 'dashboard-cache'
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_URL = 'redis://redis:6379/0'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True

    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'FileSystemCache'
    CACHE_DIR = os.path.join(Config.PROJECT_ROOT, 'debug_cache_store')
    CACHE_DEFAULT_TIMEOUT = 120

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=15)

# class TestConfig(Config):
#     """Test configuration."""
#
#     TESTING = True
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite://'
#     # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
#     BCRYPT_LOG_ROUNDS = 4
