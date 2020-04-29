
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Config:
    # Configuration object
    org_url = settings.ORG_URL

    # OpenID Specific
    grant_type = 'authorization_code'
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    issuer = settings.ISSUER
    scopes = settings.SCOPES
    redirect_uri = settings.REDIRECT_URI
    token = settings.TOKEN

class TokenManager:
    def __init__(self):
        self.idToken = None
        self.accessToken = None
        self.claims = None

    def set_id_token(self, token):
        self.idToken = token

    def set_access_token(self, token):
        self.accessToken = token

    def set_claims(self, claims):
        self.claims = claims

    def getJson(self):
        response = {}
        if self.idToken:
            response['idToken'] = self.idToken

        if self.accessToken:
            response['accessToken'] = self.accessToken

        if self.claims:
            response['claims'] = self.claims
        return response


class Advisor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=30, unique=False, default='')
    first_name = models.CharField(max_length=20, blank=True, default='')
    last_name = models.CharField(max_length=20, blank=True, default='')
    email = models.CharField(max_length=20, unique=True, default='')


    class Meta:
        verbose_name = "advisor information"
        verbose_name_plural = verbose_name
