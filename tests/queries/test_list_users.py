from unittest.mock import patch

from django.test import Client, TestCase


from .mocks import social_auth_mock

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
        self.assertEqual(
            {
                'errors': [{
                    'message': 'Permission denied',
                    'locations': [{
                        'line': 1,
                        'column': 8
                    }],
                    'path': ['users']
                }],
                'data': {
                    'users': None
                }
            }, response.json())

    @social_auth_mock
    @patch('graphql_social_auth.decorators._do_login')
    def test_user_is_logged_successfully_created(self, *args):
        body = """mutation Create {
                    login(accessToken: "token",userType:"client") {
                        user {
                        id
                        email
                        userType
                        }
                        message
                    }
                    }
                """

        response_data = {
            'data': {
                'login': {
                    'user': {
                        'id': '3',
                        'email': '',
                        'userType': 'STYLIST'
                    },
                    'message': 'You have successfully logged in '
                }
            }
        }
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    def test_user_token_is_invalid(self):
        body = """mutation Create {
                    login(accessToken: "token",userType:"client") {
                        user {
                        id
                        email
                        userType
                        }
                        token
                        message
                    }
                    }
                """
        response_data = {
            'errors': [{
                'message': "Your credentials aren't allowed",
                'locations': [{
                    'line': 2,
                    'column': 21
                }],
                'path': ['login']
            }],
            'data': {
                'login': None
            }
        }
        response = self.client.post(API_URL + '/graphql/?query=' + body)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    #
