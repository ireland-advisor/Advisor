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
    aud = settings.AUD


class Users(models.Model):
    first_name = models.CharField(max_length=50, default='non-fn', blank=False)
    last_name = models.CharField(max_length=50,  default='non-ln', blank=True)
    email = models.CharField(max_length=100, unique=True, default='', blank=False)

    class Meta:
        verbose_name = "users"
        verbose_name_plural = verbose_name




