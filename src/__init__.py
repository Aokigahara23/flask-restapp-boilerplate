import os

from flask import Flask
from flask_restful import Api

from src.config import DevConfig, ProdConfig
from src.exceptions import register_exceptions


def register_endpoints(api_ext: Api) -> None:
    """Import and register each endpoint"""

    from src.endpoints import endpoints

    for endpoint in endpoints:
        api_ext.add_resource(endpoint, endpoint.url, endpoint=endpoint.alias)


def register_extensions(app: Flask) -> None:
    """Import and initialize all flask extensions"""

    from src.extensions import database, migrate, deserializer, jwt, bcrypt, api

    database.init_app(app)
    migrate.init_app(app, database)
    deserializer.init_app(app)

    jwt.init_app(app)
    bcrypt.init_app(app)

    register_endpoints(api)
    api.init_app(app)


def create_app() -> Flask:
    """Flask app creation"""

    app = Flask('kitty-tube')

    _config = ProdConfig if os.getenv('REST_PROD_DEPLOY') else DevConfig
    app.config.from_object(_config)

    register_extensions(app)
    register_exceptions(app)

    return app
