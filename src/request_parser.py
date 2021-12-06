from argparse import Namespace
from enum import Enum
from typing import Type
from urllib.parse import urlparse, parse_qs

from src.common import HTTP_METHODS
from src.exceptions import BadArgs


class ArgLocation(Enum):
    QUERY = 'query'
    FORM = 'form'
    JSON = 'json'


class Argument:
    name: str
    location: ArgLocation
    choices: list
    type: Type = str
    required: bool = False

    def __init__(self, name, request_method: str, **options):
        self.name = name
        self.request_method = request_method
        self.location = ArgLocation.QUERY if self.request_method == HTTP_METHODS.GET else ArgLocation.FORM
        self._parse_options(**options)

    def __repr__(self):
        return '<Argument "{name}">'.format(name=self.name)

    def _parse_options(self, **options):
        for opt, value in options.items():
            setattr(self, opt, value)


# TODO: continue to polish this (maybe TDD finally? >_< )
class RequestParser:
    arguments: dict

    def __init__(self, request_method: str):
        self.request_method = request_method
        self.arguments = dict()
        self.parsed_query = dict()
        self.parsed_form_data = dict()
        self.parsed_args = dict()

    def add_argument(self, name: str, **options):
        if self.arguments.get(name) is not None:
            raise BadArgs(f'Argument {name!r} has bean already declared')

        arg = Argument(name, self.request_method, **options)
        self.arguments[arg.name] = arg

    def _parse_raw(self):
        from flask import request

        parsed_url = urlparse(request.url)
        parsed_query = parse_qs(parsed_url.query)
        self.parsed_query.update({k: v[0] if len(v) == 1 else v for k, v in parsed_query.items()})

        if request.method in [HTTP_METHODS.POST, HTTP_METHODS.PATCH] \
                or any(arg.location == ArgLocation.FORM for arg in self.arguments.values()):
            if not request.form:
                raise BadArgs(f'Form data is empty')
            self.parsed_form_data.update(request.form)

    def parse_args(self):
        self._parse_raw()

        if not self.parsed_query and not self.parsed_form_data:
            raise BadArgs('No args passed from the request')

        errors = []

        for arg in self.arguments.values():

            # TODO: better decision is request.args.get('name')
            query = self.parsed_query if arg.location == ArgLocation.QUERY else self.parsed_form_data
            parsed_value = query.get(arg.name)
            if parsed_value is None and arg.required:
                errors.append(f'Missed required argument: {arg.name}')
                continue

            if hasattr(arg, 'choices') and parsed_value not in arg.choices:
                errors.append(f'Bad choice - {parsed_value!r}. Available choices for {arg.name!r} - {arg.choices}')
                continue

            if hasattr(arg, 'type') and arg.type is not list:
                try:
                    parsed_value = arg.type(parsed_value)
                except ValueError:
                    errors.append(f'Argument expected type {arg.type!r}, got value {parsed_value!r}')
                    continue

            if hasattr(arg, 'type') and arg.type is list:
                if self.parsed_args.get(arg.name) is None:
                    self.parsed_args[arg.name] = [parsed_value]
                else:
                    self.parsed_args[arg.name].append(parsed_value)
            else:
                self.parsed_args[arg.name] = parsed_value

        if errors:
            raise BadArgs(payload=errors)

        return Namespace(**self.parsed_args)
