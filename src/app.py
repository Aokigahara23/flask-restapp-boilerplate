from typing import Type
from urllib.parse import urljoin

from flask import Flask

from src.config import Config, DevConfig
from src.extensions.errors import register_exceptions_handles


def register_endpoints(app: Flask):
    from src.endpoints import endpoints
    for endpoint in endpoints:
        endpoint.url_prefix = urljoin('/api/v1/', endpoint.url_prefix.lstrip('/'))
        app.register_blueprint(endpoint)


def register_extensions(app: Flask):
    from src.extensions import modules
    for module in modules:
        module.init_app(app)


def create_app(config: Type[Config]):
    app = Flask('vdashboard-rest-api')
    app.config.from_object(config)

    register_extensions(app)
    register_endpoints(app)
    register_exceptions_handles(app, )

    return app


if __name__ == '__main__':
    debug_app = create_app(DevConfig)
    debug_app.run(port=5000)
