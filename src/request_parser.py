from argparse import Namespace
from typing import Type, Optional, Tuple, Dict, Any

from flask import request
from flask_sqlalchemy import BaseQuery
from werkzeug.exceptions import NotFound

from src.common import HTTP_METHODS
from src.exceptions import BadArgs


class ArgLocation:
    QUERY = 'args'
    FORM = 'form'
    JSON = 'json'

    @classmethod
    def values(cls):
        return cls.__dict__.values()


class Argument:
    name: str
    location: Optional[ArgLocation]
    choices: list
    type: Type = str
    required: bool = False

    def __init__(self, name, **options):
        self.name = name
        self.location = None
        self._parse_options(**options)

    def __repr__(self) -> str:
        return '<Argument "{name}">'.format(name=self.name)

    def _parse_options(self, **options):
        for opt, value in options.items():
            if opt == 'location' and value not in ArgLocation.values():
                raise BadArgs(f'Invalid argument location : {value!r}')
            setattr(self, opt, value)


class RequestParser:
    arguments: dict

    def __init__(self):
        self.arguments = dict()
        self.parsed_args = dict()

    def add_argument(self, name: str, **options):
        if self.arguments.get(name) is not None:
            raise BadArgs(f'Argument {name!r} has bean already declared')

        arg = Argument(name, **options)
        self.arguments[arg.name] = arg

    def parse_args(self, include_only: Tuple[str] = None, ignore_required: bool = False) -> Namespace:
        """
        Parse the current request object for the given args.
        Various data location can be set to the specific argument

        :param include_only: tuple of argument names. If given will exclude all other args
            for the current parser. Implemented to use the same parser for multiple http-methods
        :param ignore_required: Will ignore required flag for the arguments.
        :return: argparse.Namespace for convenience
        """

        if include_only:
            self.arguments = {arg_name: arg for arg_name, arg in self.arguments.items() if arg_name in include_only}

        errors = []

        for arg in self.arguments.values():

            if arg.location is None:
                if request.method == HTTP_METHODS.GET:
                    arg.location = ArgLocation.QUERY
                else:
                    arg.location = ArgLocation.FORM

            query = getattr(request, arg.location)
            if query is None:
                raise BadArgs(f'No args passed from the request. Target location: {arg.location!r}')

            parsed_value = query.get(arg.name)
            if parsed_value is None:
                if arg.required and not ignore_required:
                    errors.append(f'Missed required argument: {arg.name}')
                self.parsed_args[arg.name] = parsed_value
                continue

            if hasattr(arg, 'choices') and parsed_value not in arg.choices:
                errors.append(f'Bad choice - {parsed_value!r}. Available choices for {arg.name!r} - {arg.choices}')
                continue

            if hasattr(arg, 'type') and arg.type is not list:
                try:
                    parsed_value = arg.type(parsed_value)
                except ValueError:
                    errors.append(f'Argument {arg.name!r} expected type {arg.type!r}, got value {parsed_value!r}')
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

    def has_passed_args(self, *args_to_check: str) -> bool:
        """Check that specific args were passed and have not null value"""

        if not self.parsed_args:
            return False
        return all(self.parsed_args.get(arg_name) is not None for arg_name in args_to_check)


pagination_parser = RequestParser()
pagination_parser.add_argument('page', type=int)
pagination_parser.add_argument('per_page', type=int)


def perform_pagination(query: BaseQuery) -> Tuple[BaseQuery, Dict[str, Any]]:
    """
    Try to perform a pagination operation and return a query.

    :param query: Sqlalchemy query to paginate

    :return: query and pagination data as Tuple[BaseQuery, Dict[str, Any]]
    """

    pagination_args = pagination_parser.parse_args()
    pagination_result = dict()

    if pagination_parser.has_passed_args('page', 'per_page'):
        try:
            pagination = query.paginate(pagination_args.page, pagination_args.per_page)
            query = pagination.items
            pagination_result['page'] = pagination.page
            pagination_result['per_page'] = pagination.per_page
            pagination_result['total_pages'] = pagination.pages
            pagination_result['total_items'] = pagination.total
            pagination_result['has_next'] = pagination.has_next
            pagination_result['has_prev'] = pagination.has_prev
        except NotFound:
            raise NotFound('Could not find the requested page')

    return query, pagination_result

# Will leave it here like as an interesting approach

# def pagination_attempt(model: Type[T], schema: Schema, cache: Cache = None) -> Tuple[List[dict], Dict[str, Any]]:
#     """
#     Try to perform a pagination operation and return "ready to send data", using cache.
#
#     :param model: Sqlalchemy Model inherited class. On the query of this class .paginate() will be called
#     :param schema: Schema to deserialize given query (to safely store it in the cache)
#     :param cache: if given, will store model-base query in the cache. Model-based mean next structure:
#
#         {
#             "<sub_query_name>": (
#                 deserialized Model.query,
#                 pagination_data
#             )
#         }
#
#         <sub_query_name> contain a Model name and (if pagination was passed) pagination args
#             to store specific page of a given Model.query e.g. Kitty_1_3(with_pagination) or Kitty(full_list)
#
#     :return: deserialized query of a Model (cached or not) and pagination data as Tuple[List[dict], Dict[str, Any]]
#     """
#
#     pagination_args = pagination_parser.parse_args()
#     query = model.query
#     cache_key = model.__name__
#     pagination_result = dict()
#
#     if pagination_parser.has_passed_args('page', 'per_page'):
#
#         cache_key += f'_{pagination_args.page}_{pagination_args.per_page}'
#
#         if cache is not None:
#             cached = cache.get(cache_key)
#             if cached is not None:
#                 cached_query, cached_pagination = cached
#                 return cached_query, cached_pagination
#
#         try:
#             pagination = query.paginate(pagination_args.page, pagination_args.per_page)
#             query = pagination.items
#             pagination_result['page'] = pagination.page
#             pagination_result['per_page'] = pagination.per_page
#             pagination_result['total_pages'] = pagination.pages
#             pagination_result['total_items'] = pagination.total
#             pagination_result['has_next'] = pagination.has_next
#             pagination_result['has_prev'] = pagination.has_prev
#         except NotFound:
#             raise NotFound('Could not find the requested page')
#
#     else:
#
#         if cache is not None:
#             cached = cache.get(cache_key)
#             if cached is not None:
#                 cached_query, cached_pagination = cached
#                 return cached_query, cached_pagination
#
#     query = schema.dump(query)
#
#     cache.set(cache_key, (query, pagination_result))
#
#     return query, pagination_result
