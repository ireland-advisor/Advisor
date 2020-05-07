from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from okta_jwt.jwt import generate_token

from core.decorators import okta_login_required
from core.models import Config

config = Config()
CREATE_USER_URL = reverse('user:create')


class PermissionsRequiredDecoratorTest(TestCase):
    """
    Tests for the permission_required decorator
    """

    def setUp(self):
        self.factory = RequestFactory()

        self.access_token = generate_token(config.issuer,
                                           config.client_id,
                                           config.client_secret,
                                           "leebusiness197@gmail.com",
                                           "Advisor2020")

    def test_okta_login_pass(self):
        @okta_login_required
        def a_view(request):
            return HttpResponse()

        request = self.factory.post('/rand', **{'HTTP_AUTHORIZATION': self.access_token})
        resp = a_view(request)
        self.assertEqual(resp.status_code, 200)
