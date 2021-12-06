from enum import Enum

from src.extensions import SurrogatePK, database, CRUDMixin


class CatBreed(Enum):
    BRITISH = 'british shorthair'
    MAINE_COON = 'maine coon'
    SIAM = 'siamese cat'


class Kitty(database.Model, SurrogatePK, CRUDMixin):
    """example model with enum field and relation"""

    __tablename__ = 'kitties'

    name = database.Column(database.String(20))
    age = database.Column(database.Integer)

    parent_id = database.Column(database.Integer, database.ForeignKey('kitties.id'), nullable=True)

    breed = database.Column(database.Enum(CatBreed))

    kittens = database.relationship('Kitty')

    def produce_kitten(self, name: str):
        return Kitty.create(
            name=name,
            age=0,
            breed=self.breed,
            parent_id=self.id)
