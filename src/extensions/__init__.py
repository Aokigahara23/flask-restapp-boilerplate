__all__ = ('modules', 'database', 'cache', 'migrate', 'deserializer', 'bcrypt_manager', 'jwt_manager')

from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
cache = Cache()
migrate = Migrate(db=database)
deserializer = Marshmallow()
jwt_manager = JWTManager()

modules = [
    database,
    cache,
    migrate,
    deserializer,
    jwt_manager
]
