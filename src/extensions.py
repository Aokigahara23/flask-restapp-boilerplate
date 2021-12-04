from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy, Model


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)))):
            return cls.query.get(int(record_id))

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        database.session.add(self)
        if commit:
            database.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        database.session.delete(self)
        return commit and database.session.commit()


api = Api(prefix='/api/v1')

database = SQLAlchemy()
migrate = Migrate()
deserializer = Marshmallow()

jwt = JWTManager()
bcrypt = Bcrypt()