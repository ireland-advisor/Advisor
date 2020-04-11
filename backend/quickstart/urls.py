
from django.urls import path
from quickstart import views

urlpatterns = [
    path('mentors/', views.mentor_list),
    path('mentors/<int:pk>/', views.mentor_detail),
    path('seekers/', views.seeker_list),
    path('seekers/<int:pk>/', views.seeker_detail),
]