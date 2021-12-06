import os
from urllib.parse import urljoin

from flask import Flask

from src.config import DevConfig, ProdConfig
from src.exceptions import register_exceptions


def register_endpoints(app: Flask) -> None:
    """Import and register each endpoint"""

    from src.endpoints import endpoints

    for endpoint in endpoints:
        endpoint.url_prefix = urljoin(app.config.get('APP_URL_ROOT', '/api/v1'), endpoint.url_prefix)
        app.register_blueprint(endpoint)


def register_extensions(app: Flask) -> None:
    """Import and initialize all flask extensions"""

    from src.extensions import database, migrate, deserializer, cache, search, jwt, bcrypt

    database.init_app(app)
    migrate.init_app(app, database)
    deserializer.init_app(app)
    search.init_app(app)
    cache.init_app(app)

    with app.app_context():
        cache.clear()

    jwt.init_app(app)
    bcrypt.init_app(app)

    register_endpoints(app)
    register_exceptions(app)


def create_app() -> Flask:
    """Flask app initiation"""

    app = Flask('kitty-tube', static_url_path='/api/v1')

    _config = ProdConfig if os.getenv('REST_PROD_DEPLOY') else DevConfig
    app.config.from_object(_config)

    register_extensions(app)

    return app
