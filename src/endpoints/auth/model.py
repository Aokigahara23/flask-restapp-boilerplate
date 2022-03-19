from werkzeug.security import generate_password_hash, check_password_hash

from src.extensions import database
from src.extensions.mixins import CRUDMixin


class User(database.Model, CRUDMixin):
    email = database.Column(database.String, primary_key=True, index=True)
    password_hash = database.Column(database.String, nullable=False)
    display_name = database.Column(database.String(100))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
