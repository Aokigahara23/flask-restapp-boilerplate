from http import HTTPStatus
from unittest import TestCase

from flask import Response

from src.app import create_app
from src.common import response_template
from src.config import TestConfig


class TestResponse(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def test_message_response(self):
        response_message = 'test_message'

        with self.app.app_context():
            resp = response_template(response_message, HTTPStatus.OK)
            self.assertTrue(isinstance(resp, Response))
            resp_dict: dict = resp.get_json()
            self.assertTrue('body' not in resp_dict.keys())
            self.assertTrue('message' in resp_dict.keys())
            self.assertTrue(isinstance(resp_dict['message'], str))
            self.assertTrue(resp_dict['message'] == response_message)
            self.assertTrue(resp.status_code == HTTPStatus.OK)

    def test_struct_response(self):
        response_struct = dict(foo='foo', bar='bar')

        with self.app.app_context():
            resp = response_template(response_struct, HTTPStatus.OK)
            self.assertTrue(isinstance(resp, Response))
            resp_dict: dict = resp.get_json()
            self.assertTrue('body' in resp_dict.keys())
            self.assertTrue('message' not in resp_dict.keys())
            self.assertTrue(isinstance(resp_dict['body'], dict))
            self.assertTrue(resp_dict['body'] == response_struct)
            self.assertTrue(resp.status_code == HTTPStatus.OK)

    def test_list_response(self):
        response_list = [dict(foo='foo', bar='bar'), dict(baz='baz', buz='buz')]

        with self.app.app_context():
            resp = response_template(response_list, HTTPStatus.OK)
            self.assertTrue(isinstance(resp, Response))
            resp_dict: dict = resp.get_json()
            self.assertTrue('body' in resp_dict.keys())
            self.assertTrue('message' not in resp_dict.keys())
            self.assertTrue(isinstance(resp_dict['body'], list))
            self.assertTrue(len(response_list) == len(resp_dict['body']))
            for item in resp_dict['body']:
                self.assertTrue(item in response_list)
            self.assertTrue(resp_dict['body'] == response_list)
            self.assertTrue(resp.status_code == HTTPStatus.OK)
