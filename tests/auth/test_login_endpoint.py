from http import HTTPStatus

from src.endpoints.auth.model import User
from src.extensions.errors import AUTH_ERROR
from . import AuthBase


class TestUser:
    email = 'test@test.test'
    password = '#1Test1234'
    display_name = 'test_user'


class TestLoginEndpoint(AuthBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with cls.app.app_context():
            user = User.create(save=False, email=TestUser.email, display_name=TestUser.display_name)
            user.set_password(TestUser.password)
            user.save()

    def test_successful_login(self):
        response = self.client.post('/api/v1/auth/login', json=dict(email=TestUser.email, password=TestUser.password))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_dict = response.get_json(force=True)
        self.assertTrue(isinstance(response_dict, dict))

        response_body = response_dict.get('body')
        self.assertIsNotNone(response_body)
        self.assertDictEqual(dict(email=TestUser.email, display_name=TestUser.display_name), response_body)

        additional_info = response_dict.get('additional_information')
        self.assertIsNotNone(additional_info)

    def test_incorrect_password_login(self):
        response = self.client.post('/api/v1/auth/login', json=dict(email=TestUser.email, password='incorrect'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_error = response.get_json(force=True)
        self.assertEqual(response_error.get('error'), AUTH_ERROR)

    def test_incorrect_valid_incorrect_email(self):
        response = self.client.post('/api/v1/auth/login', json=dict(email='fake@test.com', password=TestUser.password))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_error = response.get_json(force=True)
        self.assertEqual(response_error.get('error'), AUTH_ERROR)

    def test_incorrect_invalid_email(self):
        response = self.client.post('/api/v1/auth/login', json=dict(email='fake-test.com', password=TestUser.password))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_error = response.get_json(force=True)
        self.assertTrue(isinstance(response_error.get('error'), dict))
