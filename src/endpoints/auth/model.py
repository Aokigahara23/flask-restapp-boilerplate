from src.extensions import database, bcrypt, CRUDMixin


class User(database.Model, CRUDMixin):
    __tablename__ = 'users'

    email = database.Column(database.String(255), primary_key=True, unique=True)
    password_hash = database.Column(database.BINARY(128), nullable=True)
    display_name = database.Column(database.String(255), nullable=False)
    full_name = database.Column(database.String(255), nullable=True)

    def set_password(self, raw_password: str):
        self.password_hash = bcrypt.generate_password_hash(raw_password)

    def check_password(self, raw_password: str):
        return bcrypt.check_password_hash(self.password_hash, raw_password)
