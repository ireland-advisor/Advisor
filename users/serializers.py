from rest_framework import serializers
from .models import Profile, Users
from django.core.validators import EmailValidator


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'okta_id')
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]}
        }


class AdvisorSerializer(serializers.ModelSerializer):
    user_id = serializers.Field(source='user.okta_id')

    class Meta:
        model = Profile
        fields = (
            'user_id'
            'icon_url',
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
        )
