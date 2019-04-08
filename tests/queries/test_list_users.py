import json
from django.test import TestCase, Client

from apps.schema import schema

class TestListUserSchema(TestCase):
    def setUp(self):
        self.client = Client()

    def test_the_current_schema_returns_empty_list(self):
        """
        Test that the configuration works by seeing that an empty list
        is returned on querying for users
        """
        body = '''query{ users { id email phoneNumber isActive } }'''
        response = self.client.post(
            'http://127.0.0.1:8000/graphql/?query=' + body)

        self.assertIn('[]', str(response.content))
