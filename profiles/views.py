from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from core.models import MentoringTags, SeekingTags, Profile

from profiles import serializers


class BaseTagAttrViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)


class MentorTagsViewSet(BaseTagAttrViewSet):
    """Manage tags in the database"""
    queryset = MentoringTags.objects.all()
    serializer_class = serializers.MentorTagSerializer


class SeekerTagsViewSet(BaseTagAttrViewSet):
    """Manage ingredients in the database"""
    queryset = SeekingTags.objects.all()
    serializer_class = serializers.SeekingTagSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """Manage profiles in the database"""
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()

    # def get_queryset(self):
    #     """Retrieve the profiles for the authenticated user"""
    #     return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class
        ModelViewset have list and retrieve actions"""
        if self.action == 'retrieve':
            return serializers.ProfileDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new profile"""
        serializer.save(user=self.request.user)
