import string
import random

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from okta_jwt.jwt import generate_token
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Config

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


config = Config()


class PrivateUserApiTest(TestCase):
    """Test the user api (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.access_token = generate_token(config.issuer,
                                           config.client_id,
                                           config.client_secret,
                                           "leebusiness197@gmail.com",
                                           "Advisor2020")

    def test_create_valid_user_success(self):
        """test creating user with valid payload is successful"""
        email_head = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

        payload = {'email': email_head + '@gmail.com',
                   'name': 'test name'
                   }

        res = self.client.post(CREATE_USER_URL, payload, **{'HTTP_AUTHORIZATION': self.access_token})

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'user_id': 1}
        )

    def test_user_exits(self):
        """"test that user already exits failed"""
        payload = {'email': 'lee@gmail.com',
                   'name': 'Test'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload, **{'HTTP_AUTHORIZATION': self.access_token})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
