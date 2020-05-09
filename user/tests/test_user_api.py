import string
import random

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user api (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test creating user with valid payload is successful"""
        email_head = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

        payload = {'email': email_head + '@gmail.com',
                   'first_name': 'test name',
                   'last_name': 'last_name'
                   }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'user_id': 1}
        )

    def test_user_exits(self):
        """"test that user already exits failed"""
        payload = {'email': 'lee@gmail.com',
                   'first_name': 'Test',
                   'last_name': 'Test'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
