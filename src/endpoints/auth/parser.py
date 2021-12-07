from src.request_parser import RequestParser

auth_parser = RequestParser()
auth_parser.add_argument('email', required=True)
auth_parser.add_argument('password', required=True)
auth_parser.add_argument('display_name', required=True)
auth_parser.add_argument('full_name')
