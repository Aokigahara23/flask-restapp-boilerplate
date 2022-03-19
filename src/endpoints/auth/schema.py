import re

from marshmallow import fields

from src.extensions import deserializer
from .model import User

PASSWORD_VALIDATE_REGEX = re.compile(r'^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
EMAIL_VALIDATE_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def validate_email(email: str) -> bool:
    return bool(EMAIL_VALIDATE_REGEX.fullmatch(email))


def validate_password(password: str) -> bool:
    return bool(PASSWORD_VALIDATE_REGEX.match(password))


class LoginSpec(deserializer.Schema):
    email = fields.String(validate=validate_email, required=True)
    password = fields.String(required=True)


class RegisterSpec(deserializer.Schema):
    email = fields.String(validate=validate_email, required=True)
    password = fields.String(required=True, validate=validate_password)


class UserSchema(deserializer.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password_hash',)
