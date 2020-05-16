from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from okta_jwt.jwt import validate_token, generate_token
from rest_framework import authentication
from rest_framework import exceptions

from core.models import Config

config = Config()


class OktaAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        if not access_token:
            return None
        # access_token = generate_token(config.issuer, config.client_id, config.client_secret, "leebusiness197@gmail.com",
        #                               "Advisor2020")
        # print(access_token)
        payload = validate_token(access_token, config.issuer, config.aud, config.client_id)

        try:
            user = get_user_model().objects.get(email=payload['sub'])

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
