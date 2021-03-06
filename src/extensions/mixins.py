from flask_sqlalchemy import Model

from . import database


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, save: bool = True, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        if not save:
            return instance
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


class SurrogatePK(object):
    """
    A mixin that adds a surrogate integer 'primary key' column named `id`
        to any declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = database.Column(database.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)))):
            return cls.query.get(int(record_id))
