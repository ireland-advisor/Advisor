from django.db import models
from django.conf import settings

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
    aud = settings.AUD


class Users(models.Model):
    first_name = models.CharField(max_length=50, default='non-fn', blank=False)
    last_name = models.CharField(max_length=50,  default='non-ln', blank=True)
    email = models.CharField(max_length=100, unique=True, default='', blank=False)

    class Meta:
        verbose_name = "users"
        verbose_name_plural = verbose_name


class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name="user", blank=False)
    icon_url = models.TextField()
    gender = models.CharField("gender", blank=True, max_length=6, choices=GENDER_CHOICES, default="female")
    personal_des = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    birthday = models.DateField("year-month-day", null=True, blank=True)
    mentoring_fields = models.TextField(default='non')
    seeking_fields = models.TextField(default='non')
    isAvailable = models.BooleanField(default=False)
    language = models.CharField(default='english', max_length=100)

    university = models.CharField(max_length=50, default='non')
    degree = models.CharField(max_length=50, default='non')

    country = models.CharField(max_length=50, default='non')
    city = models.CharField(max_length=50, default='non')

    current_business_title = models.TextField(default='non')
    industry = models.CharField(max_length=50, default='non')
    working_experience = models.TextField(default='non')

    class Meta:
        ordering = ['created']
        verbose_name = "profile"
        verbose_name_plural = verbose_name


