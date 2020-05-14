from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from advisor_api import settings


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


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """create and save a new user"""
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default="non", blank=True)
    last_name = models.CharField(max_length=255, default="non", blank=True)
    okta_id = models.CharField(max_length=255, default="0")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class SeekingTags(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class MentoringTags(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


GENDER_CHOICES = (("0", "male"), ("1", "female"))


class Profile(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    gender = models.CharField("gender",
                              max_length=55,
                              blank=True,
                              choices=GENDER_CHOICES,
                              default="female")
    personal_des = models.TextField(max_length=255, blank=True)
    birthday = models.DateField("year-month-day", blank=True)
    seeking_tags = models.ManyToManyField('SeekingTags')
    mentoring_tags = models.ManyToManyField('MentoringTags')
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title
