
from django.urls import path,include
from users import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('mentors/', views.mentor_list),
    path('mentors/<int:pk>/', views.mentor_detail),
    path('seekers/', views.seeker_list),
    path('seekers/<int:pk>/', views.seeker_detail),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]