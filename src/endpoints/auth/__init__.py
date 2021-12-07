from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from src.common import response_template, HTTP_METHODS, HTTP_STATUS
from src.exceptions import error_response
from src.extensions import cache
from .model import User
from .parser import auth_parser
from .schema import UserSchema

auth_endpoint = Blueprint('auth', __name__)


# /register

@auth_endpoint.route('/register', methods=(HTTP_METHODS.POST,))
def register():
    args = auth_parser.parse_args()
    user = User.create(
        save=False,
        email=args.email,
        display_name=args.display_name,
        full_name=args.full_name)

    user.set_password(args.password)
    user.save()

    return response_template(
        UserSchema().dump(user),
        HTTP_STATUS.CREATED)


# /login

@auth_endpoint.route('/login', methods=(HTTP_METHODS.POST,))
def login():
    args = auth_parser.parse_args(include_only=('email', 'password'))
    user = User.query.get(args.email)
    if user is None or not user.check_password(args.password):
        return error_response(
            f'Authentications failed',
            HTTP_STATUS.UNAUTHORIZED)

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return response_template(
        UserSchema().dump(user),
        HTTP_STATUS.OK,
        None, access_token=access_token,
        refresh_token=refresh_token)


@auth_endpoint.route('/login', methods=(HTTP_METHODS.GET,))
@jwt_required()
@cache.cached(key_prefix='check_auth')
def check_auth():
    user_email = get_jwt_identity()
    user = User.query.get(user_email)

    return response_template(
        UserSchema().dump(user),
        HTTP_STATUS.OK)
