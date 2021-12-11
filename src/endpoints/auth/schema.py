from src.extensions import deserializer
from .model import User


class UserSchema(deserializer.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password_hash",)
