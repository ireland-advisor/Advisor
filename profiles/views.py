from rest_framework import viewsets, mixins

from core.models import MentoringTags, SeekingTags

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
