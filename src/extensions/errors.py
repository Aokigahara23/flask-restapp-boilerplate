from http import HTTPStatus
from typing import Union

from flask import make_response, Response, Flask
from webargs import ValidationError
from webargs.flaskparser import parser
from werkzeug.exceptions import BadRequest

from src.extensions import jwt_manager

AUTH_ERROR = 'Authentication failed'


def error_response(message: Union[str, dict],
                   status_code: int,
                   **additional_information: dict) -> Response:
    """Common error response to ensure that API error output has the same format"""
    common_struct = dict(error=message, status_code=status_code, additional_information=additional_information)
    resp = make_response(common_struct, status_code)
    return resp


def item_not_found_response(item_repr: str, searched_id: Union[str, int] = None) -> Response:
    if searched_id is not None:
        item_repr += f'(id: {searched_id!r})'
    return error_response(f'Could not find item <{item_repr}>', HTTPStatus.NOT_FOUND)


def auth_error():
    return error_response(AUTH_ERROR, HTTPStatus.UNAUTHORIZED)


def register_exceptions_handles(app: Flask):
    @app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
    def not_allowed(e) -> Response:
        return error_response(str(e), HTTPStatus.METHOD_NOT_ALLOWED)

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(e) -> Response:
        return error_response(str(e), HTTPStatus.NOT_FOUND)

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_error(e) -> Response:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(e) -> Response:
        return error_response(e.response, HTTPStatus.BAD_REQUEST)

    @parser.error_handler
    def handle_error(error: ValidationError, req, schema, *, error_status_code, error_headers):
        error = error.messages.get('json')

        raise BadRequest('Invalid args were passed', response=error)

    @jwt_manager.expired_token_loader
    def expired_token_response(*args) -> Response:
        return auth_error()

    @jwt_manager.invalid_token_loader
    def invalid_token_response(*args) -> Response:
        return auth_error()

    @jwt_manager.unauthorized_loader
    def no_jwt_is_present(*args) -> Response:
        return auth_error()
