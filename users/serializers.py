
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import Mentor, Seeker

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['first_name','gender','title','des','expertiseFields','isAvailable']


class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ['first_name','gender','title','des','seekingFields']
