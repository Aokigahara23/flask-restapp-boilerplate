from marshmallow_enum import EnumField

from src.extensions import deserializer
from .model import Kitty, CatBreed


class KittySchema(deserializer.SQLAlchemyAutoSchema):
    """example marshmallow schema to deserialize sqlalchemy model with enum and relation"""

    class Meta:
        model = Kitty

    breed = EnumField(CatBreed, by_value=True)
    kittens = deserializer.Nested('KittySchema', many=True)

    _links = deserializer.Hyperlinks(
        {
            "self": deserializer.URLFor("kitties.get_kitty", values=dict(kitty_id="<id>")),
            "parent": deserializer.URLFor("kitties.get_kitty", values=dict(kitty_id="<parent_id>"))
        }
    )
