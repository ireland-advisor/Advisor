from rest_framework import serializers
from .models import Users
from django.core.validators import EmailValidator


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, error_messages={"required": "first_name can't be null"})
    last_name = serializers.CharField(required=True, error_messages={"required": "last_name can't be null"})
    email = serializers.CharField(required=True, error_messages={"required": "email can't be null"})

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]}
        }