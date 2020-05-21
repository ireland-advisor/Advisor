import string
import random
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def activate_url():
    """Return profile detail URL"""
    return "%s?okta_id=test" % reverse('user:activate')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user api (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    @patch('user.views.send_email')
    @patch('user.views.create_okta_user')
    def test_create_valid_user_success(self, create_okta_user_metod, send_email_method):
        """test creating user with valid payload is successful"""

        create_okta_user_metod.return_value = "OKTAUSERIDHAHAHAHA"

        email_head = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

        payload = {'email': email_head + '@gmail.com',
                   'first_name': 'fisrt name',
                   'last_name': 'last name',
                   'password': 'testpw'
                   }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'result': {'okta_user_id': 'OKTAUSERIDHAHAHAHA'}}
        )

    def test_user_exits(self):
        """"test that user already exits failed"""
        payload = {'email': 'lee@gmail.com',
                   'first_name': 'Test',
                   'last_name': 'Test',
                   'password': 'password'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('user.views.activate_okta_user')
    def test_activate_user_successfully(self, patch_method):
        patch_method.return_value = 0
        url = activate_url()
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'result': {'activated_user_id': 0}}
        )

    @patch('user.views.activate_okta_user')
    def test_activate_user_fail(self, patch_method):
        patch_method.side_effect = Exception("wrong")
        url = activate_url()
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


