from http import HTTPStatus
from typing import Dict, Any

from flask import Response, make_response

HTTP_STATUS = HTTPStatus


def response_template(data: Dict[str, Any],
                      status_code: int,
                      extra_headers: Dict[str, str] = None,
                      **additional_information: Dict[str, Any]) -> Response:
    common_struct = dict(body=data, status_code=status_code, additional_information=additional_information)
    resp = make_response(common_struct, status_code)
    resp.headers.extend(extra_headers or {})
    return resp
