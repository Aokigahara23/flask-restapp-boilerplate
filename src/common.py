from typing import Union, Dict, Any

from flask import make_response, Response


class HttpMethods:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


def response_template(data: Union[dict, list, str],
                      status_code: int,
                      extra_headers: Dict[str, str] = None,
                      **additional_information: Dict[str, Any]) -> Response:
    """Common response template to ensure any correct API output has the same format"""
    common_struct = dict(status_code=status_code, additional_information=additional_information)
    if isinstance(data, str):
        common_struct['message'] = data
    else:
        common_struct['body'] = data

    resp = make_response(common_struct, status_code)
    resp.headers.extend(extra_headers or {})
    return resp
