from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from webargs.flaskparser import use_args

from src.common import HttpMethods, response_template
from src.extensions.errors import auth_error
from .model import User
from .schema import UserSchema, LoginSpec

auth_endpoint = Blueprint('auth', 'auth', url_prefix='/auth')


@auth_endpoint.route('/login', methods=(HttpMethods.POST,))
@use_args(LoginSpec)
def login(args):
    user = User.query.get(args.get('email'))
    if user is None or not user.check_password(args.get('password')):
        return auth_error()

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    return response_template(UserSchema().dump(user),
                             HTTPStatus.OK,
                             access_token=access_token,
                             refresh_token=refresh_token)
