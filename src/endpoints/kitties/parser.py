from src.request_parser import RequestParser
from .model import CatBreed

kitty_list_parser = RequestParser()
kitty_list_parser.add_argument('name', required=True)
kitty_list_parser.add_argument('age', type=int, required=True)
kitty_list_parser.add_argument('breed', type=str, required=True, choices=[breed.name for breed in CatBreed])
