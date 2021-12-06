from http import HTTPStatus
from typing import Dict, Any

from flask import Response, make_response

APP_ROOT = '/api/v1'

HTTP_STATUS = HTTPStatus


class HttpMethods:
    POST = 'POST'
    GET = 'GET'
    UPDATE = 'UPDATE'
    PATCH = 'PATCH'


HTTP_METHODS = HttpMethods


def response_template(data: Dict[str, Any],
                      status_code: int,
                      extra_headers: Dict[str, str] = None,
                      **additional_information: Dict[str, Any]) -> Response:
    """Common response template to ensure any correct API output has the same format"""
    common_struct = dict(body=data, status_code=status_code, additional_information=additional_information)
    resp = make_response(common_struct, status_code)
    resp.headers.extend(extra_headers or {})
    return resp
