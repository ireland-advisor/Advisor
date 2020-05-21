from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create', views.CreateUserView.as_view(), name='create'),
    path('email_verify', views.ActivateUser.as_view(), name='activate'),
]
