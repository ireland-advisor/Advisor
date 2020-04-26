from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from .models import Advisor
from .serializer import CreateUserSerializer


# class OauthTest(APITestCase):
#     def setUp(self) -> None:
#         self.email = "nothing1@gmail.com"
#         self.username = "lee"
#         self.firstname = 'qi'
#         self.lastname = 'li'
#         self.user_url = reverse("register")
#
#         self.user = Advisor.objects.create(email=self.email,
#                                            user_name=self.username,
#                                            first_name=self.firstname,
#                                            last_name=self.lastname)
#
#     def tearDown(self) -> None:
#         self.user.delete()
#
#     def test_post_user_info(self):
#         user_serializer_data = json.dumps(CreateUserSerializer(instance=self.user).data)
#         resp = self.client.post(self.user_url, user_serializer_data, content_type='application/json')
#         breakpoint()
#         self.assertEqual(200, resp.status_code)
#         self.assertIn(self.user.user_name.encode(), resp.content)
