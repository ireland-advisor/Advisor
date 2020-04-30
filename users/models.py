from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.conf import settings

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
GENDER_CHOICES = (("0", "male"), ("1", "female"))


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
    icon_url = models.TextField()
    gender = models.CharField("gender", max_length=6, choices=GENDER_CHOICES, default="female")
    personal_des = models.TextField(blank=False)
    tags = models.TextField()
    birthday = models.DateField("year-month-day", null=True, blank=True)
    mentoringFields = models.TextField(default='non')
    seekingFields = models.TextField(default='non')
    isAvailable = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)

    university = models.CharField(max_length=50, default='non')
    degree = models.CharField(max_length=50, default='non')

    country = models.CharField(max_length=50, default='non')
    city = models.CharField(max_length=50, default='non')

    current_business_title = models.TextField(default='non')
    industry = models.CharField(max_length=50, default='non')
    working_experience = models.TextField(default='non')

    class Meta:
        ordering = ['created']
        verbose_name = "advisor"
        verbose_name_plural = verbose_name


class Users(models.Model):
    first_name = models.CharField(max_length=20, blank=True, default='')
    last_name = models.CharField(max_length=20, blank=True, default='')
    email = models.CharField(max_length=20, unique=True, default='')
    okta_id = models.CharField(max_length=20, blank=True, default='0')


    class Meta:
        verbose_name = "user auth information"
        verbose_name_plural = verbose_name