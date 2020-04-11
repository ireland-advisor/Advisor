from rest_framework import serializers
from quickstart.models import Mentor, Seeker


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['name','gender','title','des','expertiseFields','isAvailable','language']


class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        fields = ['name','gender','title','des','seekingFields','language']