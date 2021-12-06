from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.common import response_template, HTTP_STATUS, HTTP_METHODS
from src.exceptions import item_not_found_response
from src.extensions import cache
from .model import Kitty, CatBreed
from .parser import kitty_list_parser
from .schema import KittySchema

kitties = Blueprint('kitties', __name__, url_prefix='kitties')


# /kitties

@kitties.route('', methods=(HTTP_METHODS.GET,))
@jwt_required()
@cache.cached(key_prefix='all_kitties')
def get_kitties():
    return response_template(
        KittySchema(many=True).dump(Kitty.query),
        HTTP_STATUS.OK)


@kitties.route('', methods=(HTTP_METHODS.POST,))
@jwt_required()
def create_kitty():
    args = kitty_list_parser.parse_args()
    kitty = Kitty.create(name=args.name, age=args.age, breed=CatBreed[args.breed])

    cache.delete('all_kitties')

    return response_template(
        KittySchema().dump(kitty),
        HTTP_STATUS.CREATED)


# /kitties/id
@kitties.route('/<int:kitty_id>', methods=(HTTP_METHODS.GET,))
@jwt_required()
def get_kitty(kitty_id: int):
    kitty = Kitty.query.get(kitty_id)
    if kitty is None:
        return item_not_found_response(Kitty.__name__, kitty_id)

    return response_template(
        KittySchema().dump(kitty),
        HTTP_STATUS.OK)


@kitties.route('/<int:kitty_id>', methods=(HTTP_METHODS.PATCH,))
@jwt_required()
def produce_kitten(kitty_id: int):
    kitty = Kitty.query.get(kitty_id)
    if kitty is None:
        return item_not_found_response(Kitty.__name__, kitty_id)

    kitten = kitty.produce_kitten('Luke')

    return response_template(
        KittySchema().dump(kitten),
        HTTP_STATUS.OK)
