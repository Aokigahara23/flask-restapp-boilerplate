from typing import Optional, Dict, Any, Union

from flask import Response, make_response, Flask
from werkzeug.exceptions import Conflict

from src.common import HTTP_STATUS
from src.extensions import jwt


def error_response(error: Union[str, Dict[str, Any]],
                   status_code: int,
                   extra_headers: Optional[Dict[str, str]] = None,
                   return_dict: bool = False,
                   **additional_information: Dict[str, Any]) -> Union[Response, dict]:
    """Common error response to ensure that API error output has the same format"""
    common_struct = dict(error=error, status_code=status_code, additional_information=additional_information)
    if return_dict:
        return common_struct
    resp = make_response(common_struct, status_code)
    resp.headers.extend(extra_headers or {})
    return resp


def item_not_found_response(item_repr: str, searched_id: Union[str, int] = None) -> Response:
    if searched_id is not None:
        item_repr += f'(id: {searched_id!r})'
    return error_response(f'Could not find item <{item_repr}>', HTTP_STATUS.NOT_FOUND)


@jwt.expired_token_loader
def expired_token_response(*args) -> Response:
    return error_response(f'Token has expired', HTTP_STATUS.UNAUTHORIZED)


@jwt.invalid_token_loader
def invalid_token_response(error) -> Response:
    return error_response(error, HTTP_STATUS.UNAUTHORIZED)


@jwt.unauthorized_loader
def no_jwt_is_present(error):
    return error_response(error, HTTP_STATUS.UNAUTHORIZED)


class BadArgs(Conflict):
    payload: Dict[str, Any]

    def __init__(self, description: str = None, payload: Any = None, *args, **kwargs):
        super().__init__(description=description, *args, **kwargs)
        self.payload = payload


def register_exceptions(app: Flask) -> None:
    @app.errorhandler(HTTP_STATUS.METHOD_NOT_ALLOWED)
    def not_allowed(e):
        return error_response(str(e), HTTP_STATUS.METHOD_NOT_ALLOWED)

    @app.errorhandler(HTTP_STATUS.NOT_FOUND)
    def not_found(e):
        return error_response(str(e), HTTP_STATUS.NOT_FOUND)

    @app.errorhandler(HTTP_STATUS.INTERNAL_SERVER_ERROR)
    def internal_error(e):
        return error_response(str(e), HTTP_STATUS.INTERNAL_SERVER_ERROR)

    @app.errorhandler(HTTP_STATUS.CONFLICT)
    def invalid_args_passed(e):
        err_dict = dict(message='Invalid request arguments')
        if e.description is not None:
            err_dict['details'] = e.description
        if hasattr(e, 'payload') and e.payload:
            err_dict['payload'] = e.payload
        return error_response(err_dict, HTTP_STATUS.BAD_REQUEST)
