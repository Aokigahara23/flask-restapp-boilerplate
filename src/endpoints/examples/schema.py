from marshmallow_enum import EnumField

from src.extensions import deserializer
from .model import Kitty, CatBreed


class KittySchema(deserializer.SQLAlchemyAutoSchema):
    """example marshmallow schema to deserialize sqlalchemy model with enum and relation"""

    class Meta:
        model = Kitty

    breed = EnumField(CatBreed, by_value=True)
    kittens = deserializer.Nested('KittySchema', many=True)
