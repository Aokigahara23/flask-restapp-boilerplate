from src.common import HTTP_METHODS
from src.request_parser import RequestParser

login_parser = RequestParser(HTTP_METHODS.POST)
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)

reg_parser = RequestParser(HTTP_METHODS.POST)
reg_parser.add_argument('email', required=True)
reg_parser.add_argument('password', required=True)
reg_parser.add_argument('display_name', required=True)
reg_parser.add_argument('full_name')
