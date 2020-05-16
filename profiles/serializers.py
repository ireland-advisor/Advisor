from rest_framework import serializers
from core.models import MentoringTags, SeekingTags, Profile

class SeekingTagSerializer(serializers.ModelSerializer):
    """Serializer for seeker object"""

    class Meta:
        model = SeekingTags
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class MentorTagSerializer(serializers.ModelSerializer):
    """Serializer for an mentor object"""

    class Meta:
        model = MentoringTags
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize a profile"""
    seeking_tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SeekingTags.objects.all(),
        required=False
    )
    mentoring_tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MentoringTags.objects.all(),
        required=False
    )

    class Meta:
        model = Profile
        fields = (
            'id', 'title', 'gender', 'seeking_tags', 'mentoring_tags', 'personal_des', 'birthday',
            'is_available',
        )
        read_only_Fields = (id,)


class ProfileDetailSerializer(ProfileSerializer):
    seeking_tags = SeekingTagSerializer(many=True, read_only=True)
    mentoring_tags = MentorTagSerializer(many=True, read_only=True)
