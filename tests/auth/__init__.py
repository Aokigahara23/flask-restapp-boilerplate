import os
from unittest import TestCase

from src.app import create_app
from src.config import TestConfig
from src.extensions import database


class AuthBase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            database.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        with cls.app.app_context():
            database.drop_all()
            os.remove(TestConfig.DB_PATH)
