from rest_framework import serializers
from .models import Advisor, Users
from django.core.validators import EmailValidator


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]}
        }


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = [
            'icon_url',
            'personal_des',
            'tags',
            'gender',
            'personal_des',
            'birthday',
            'mentoring_fields',
            'seeking_fields',
            'isAvailable',
            'language',
            'university',
            'degree',
            'country',
            'city',
            'current_business_title',
            'industry',
            'working_experience'
        ]
