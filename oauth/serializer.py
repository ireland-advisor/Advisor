from django.core.validators import EmailValidator
from rest_framework import serializers
from django.contrib.auth.models import User

from oauth.models import Advisor


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('first_name', 'last_name', 'email', 'user_name')
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]}
        }
