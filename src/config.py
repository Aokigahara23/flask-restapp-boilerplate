"""Application configuration."""
import os
from datetime import timedelta


def get_host_uri():
    hostname = os.getenv('VDASHBOARD_DB_HOST')
    username = os.getenv('VDASHBOARD_DB_USER_NAME')
    password = os.getenv('VDASHBOARD_DB_PASSWORD')
    db_name = os.getenv('VDASHBOARD_DB_NAME')
    db_port = os.getenv('VDASHBOARD_DB_PORT') or 5432
    return f'{username}:{password}@{hostname}:{db_port}/{db_name}'


class Config(object):
    """Base configuration."""

    # FLASK_COMMON
    SECRET_KEY = os.environ.get('VDASHBOARD_SECRET_KEY', os.urandom(64))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BUNDLE_ERRORS = True

    # SQLALCHEMY COMMON
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:5000',
        'http://localhost:5000'
    ]


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False

    # DB
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{get_host_uri()}?charset=utf8mb4'

    # CACHE
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 500
    CACHE_REDIS_HOST = 'redis-container'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_DB = 'dashboard-cache'
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_URL = 'redis://redis:6379/0'

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True

    # DB
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}?check_same_thread=False&?charset=utf8mb4'
    SQLALCHEMY_ECHO = True

    # CACHE
    CACHE_TYPE = 'FileSystemCache'
    CACHE_DIR = os.path.join(Config.PROJECT_ROOT, 'debug_cache_store')
    CACHE_DEFAULT_TIMEOUT = 120

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=15)


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True

    # DB
    BCRYPT_LOG_ROUNDS = 4
    DB_NAME = 'test.dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}?check_same_thread=False&?charset=utf8mb4'

    # CACHE
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 120

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=15)
