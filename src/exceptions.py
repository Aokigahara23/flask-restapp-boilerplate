from typing import Optional, Dict, Any, Union

from flask import Response, Flask, make_response

from src.common import HTTP_STATUS
from src.extensions import jwt


def error_response(message: str,
                   status_code: int,
                   extra_headers: Optional[Dict[str, str]] = None,
                   **additional_information: Dict[str, Any]) -> Response:
    common_struct = dict(error_message=message, status_code=status_code, additional_information=additional_information)
    resp = make_response(common_struct, status_code)
    resp.headers.extend(extra_headers or {})
    return resp


def item_not_found_response(item_repr: str, searched_id: Union[str, int] = None) -> Response:
    if searched_id is not None:
        item_repr += f'(id: {searched_id!r})'
    return error_response(f'Could not find item <{item_repr}>', HTTP_STATUS.NOT_FOUND)


# TODO: debug this and make it more informative (in a right way)
@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload) -> Response:
    return error_response(f'Token: {jwt_header} - {jwt_payload} has expired', HTTP_STATUS.UNAUTHORIZED)


@jwt.invalid_token_loader
def invalid_token_response(error) -> Response:
    return error_response(error, HTTP_STATUS.UNAUTHORIZED)


@jwt.unauthorized_loader
def no_jwt_is_present(error):
    return error_response(error, HTTP_STATUS.UNAUTHORIZED)


def register_exceptions(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return error_response(str(e), HTTP_STATUS.NOT_FOUND)
