from unittest import mock
from unittest.mock import patch

from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from okta_jwt.jwt import generate_token
from rest_framework.utils import json

from core.decorators import okta_login_required, check_token
from core.models import Config

config = Config()
CREATE_USER_URL = reverse('user:create')


class PermissionsRequiredDecoratorTest(TestCase):
    """
    Tests for the permission_required decorator
    """

    def setUp(self):
        self.factory = RequestFactory()

        self.request = self.factory.post('/rand', **{'HTTP_AUTHORIZATION': "mock_token"})

    def test_okta_login_called(self):
        @okta_login_required
        def a_view(request):
            return HttpResponse()

        request = self.factory.post('/rand')
        resp = a_view(request)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(json.loads(resp.content), {"result": "HTTP_AUTHORIZATION required"})

    @patch('core.decorators.validate_token')
    def test_check_token_passed(self, patch_method):
        result, message = check_token(self.request)
        self.assertTrue(result)
        self.assertTrue(patch_method)

    @patch('core.decorators.validate_token')
    def test_check_token_failed(self, patch_method):
        patch_method.side_effect = Exception("error on validating")
        result, message = check_token(self.request)
        self.assertFalse(result)
        self.assertEqual(message.status_code, 400)
