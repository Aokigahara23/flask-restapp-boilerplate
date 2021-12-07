from .model import User
from src.extensions import deserializer


class UserSchema(deserializer.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password_hash",)
