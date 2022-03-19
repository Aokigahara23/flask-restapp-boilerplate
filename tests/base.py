import os
from typing import Union
from unittest import TestCase

from flask import Response

from src.app import create_app
from src.config import TestConfig
from src.extensions import database


class BaseTest(TestCase):

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

    def check_response(self, response: Response, status_code: int,
                       body: Union[str, dict],
                       additional_info: list = None):
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status_code)

        response_dict: dict = response.get_json(force=True)
        self.assertIsNotNone(response_dict)
        self.assertTrue('body' in response_dict.keys() if isinstance(body, dict) else 'message' in response_dict.keys())
        self.assertTrue('status_code' in response_dict.keys())
        self.assertEqual(response_dict.get('status_code'), status_code)

        if isinstance(body, str):
            self.assertEqual(body, response_dict.get('message'))
        else:
            self.assertEqual(len(body.keys()), len(response_dict.get('body').keys()))
            for key, value in body.items():
                pass
