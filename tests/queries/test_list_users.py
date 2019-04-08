import json
from unittest.mock import Mock, patch

from django.test import Client, TestCase

from apps.schema import schema
from tests.factories.users import UserFactory

API_URL = "http://127.0.0.1:8000"


class TestListUserSchema(TestCase):
    def setUp(self):
        self.client = Client()

    def test_the_current_schema_returns_empty_list(self):
        """
        Test that the configuration works by seeing that an empty list
        is returned on querying for users
        """
        body = '''query{ users { id email phoneNumber isActive } }'''
        response = self.client.post(API_URL + '/graphql/?query=' + body)

        self.assertIn('[]', str(response.content))

    @patch('apps.users.google.Generate_User.decode_token')
    def test_user_is_logged_successfully_created(self, mock_post):
        mock_post.return_value = {"email": "kimbsimon2@gmail.com"}
        body = """mutation createuser {
                createUser(googleToken: "123456",phoneNumber:"2567249764509",userType:"client") {
                    user {
                    phoneNumber
                    email
                    }
                    message
                    }
                }
                """
        response_data = {
            'data': {
                'createUser': {
                    'user': {
                        'phoneNumber': '2567249764509',
                        'email': 'kimbsimon2@gmail.com'
                    },
                    'message': 'You have successfully signed up'
                }
            }
        }
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    @patch('apps.users.google.requests.get')
    def test_user_token_is_invalid(self, mock_get):
        mock_get.return_value.status_code.return_value = 400
        body = """mutation createuser {
                createUser(googleToken: "123456",phoneNumber:"+12249764509",userType:"client") {
                    user {
                    phoneNumber
                    email
                    }
                    message
                    }
                }
                """
        response_data = {
            'errors': [{
                'message': 'Invalid token Id',
                'locations': [{
                    'line': 2,
                    'column': 17
                }],
                'path': ['createUser']
            }],
            'data': {
                'createUser': None
            }
        }
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    @patch('apps.users.google.requests.get')
    def test_user_token_is_valid(self, mock_get):
        mock_get.return_value.status_code.return_value = 200
        body = """mutation createuser {
                createUser(googleToken: "123456",phoneNumber:"+12249764509", userType:"client") {
                    user {
                    phoneNumber
                    email
                    }
                    message
                    }
                }
                """
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)

    @patch('apps.users.google.Generate_User.decode_token')
    def test_user_login(self, mock_get):
        user = UserFactory(email='kimbsimon2@gmail.com',
                           phone_number="+12249764509")
        user.create_user()
        mock_get.return_value = {"email": "kimbsimon2@gmail.com"}
        body = """mutation createuser {
                createUser(googleToken: "123456",userType:"client") {
                    user {
                    phoneNumber
                    email
                    }
                    message
                    }
                }
                """
        response_data = {
            'data': {
                'createUser': {
                    'user': {
                        'phoneNumber': '+12249764509',
                        'email': 'kimbsimon2@gmail.com'
                    },
                    'message': 'You have successfully logged in'
                }
            }
        }
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    @patch('apps.users.google.Generate_User.decode_token')
    def test_user_signUp_with_existing_no(self, mock_get):
        user = UserFactory(email='kimbsimon2@gmail.com',
                           phone_number="12249764509")
        user.create_user()
        mock_get.return_value = {"email": "kimbugwe@gmail.com"}
        body = """mutation createuser {
                createUser(googleToken: "123456",phoneNumber:"12249764509",userType:"client") {
                    user {
                    phoneNumber
                    email
                    }
                    message
                    }
                }
                """
        response_data = {
            'errors': [{
                'message': 'User with the same phone number exists',
                'locations': [{
                    'line': 2,
                    'column': 17
                }],
                'path': ['createUser']
            }],
            'data': {
                'createUser': None
            }
        }
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json(), response_data)
