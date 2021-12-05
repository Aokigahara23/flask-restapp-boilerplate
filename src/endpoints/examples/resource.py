from flask_restful import Resource, reqparse

from src.common import response_template, HTTP_STATUS
from src.exceptions import item_not_found_response
from .model import Kitty, CatBreed
from .schema import KittySchema


class KittyListEP(Resource):
    """Example API resource for a list of objects"""

    url: str = '/kitties'
    alias = 'kitties'

    def __init__(self):
        breed_choices = (choice.value for choice in CatBreed)

        self.request_parser = reqparse.RequestParser(bundle_errors=True)
        self.request_parser.add_argument('name', type=str, required=True, help='Kitty has to have a name')
        self.request_parser.add_argument('breed', type=str, choices=breed_choices, help='Specify the breed of the cat')
        self.request_parser.add_argument('age', type=int, default=5)

    def get(self):
        return response_template(KittySchema(many=True).dump(Kitty.query), HTTP_STATUS.OK)

    def post(self):
        args = self.request_parser.parse_args()

        kitty = Kitty.create(name=args.name, breed=CatBreed(args.breed), age=args.age)
        return response_template(KittySchema().dump(kitty), HTTP_STATUS.CREATED)


class KittyEP(Resource):
    """Example API resource for a specific object"""

    url: str = '/kitties/<int:kitty_id>'
    alias = 'kitty'

    def get(self, kitty_id: int):
        kitty = Kitty.get_by_id(kitty_id)
        if kitty is None:
            return item_not_found_response(Kitty.__name__, kitty_id)
        return response_template(KittySchema().dump(kitty), HTTP_STATUS.OK)

    def patch(self, kitty_id: int):
        kitty = Kitty.get_by_id(kitty_id)
        if kitty is None:
            return item_not_found_response(Kitty.__name__, kitty_id)
        kitten = kitty.produce_kitten('Leia')
        return response_template(KittySchema().dump(kitten), HTTP_STATUS.CREATED)
