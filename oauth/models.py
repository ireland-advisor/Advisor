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


class Advisor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=30, unique=False, default='')
    first_name = models.CharField(max_length=20, blank=True, default='')
    last_name = models.CharField(max_length=20, blank=True, default='')
    email = models.CharField(max_length=20, unique=True, default='')


    class Meta:
        verbose_name = "advisor information"
        verbose_name_plural = verbose_name
