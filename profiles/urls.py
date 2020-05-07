from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles import views

router = DefaultRouter()
router.register('mentor_tags', views.MentorTagsViewSet)
router.register('seeker_tags', views.SeekerTagsViewSet)

app_name = 'profile'

urlpatterns = [
    path('', include(router.urls))
]
