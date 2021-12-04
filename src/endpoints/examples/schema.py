from src.extensions import deserializer
from .model import Kitty


class KittySchema(deserializer.SQLAlchemyAutoSchema):
    class Meta:
        model = Kitty
