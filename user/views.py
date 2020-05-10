from django.http import JsonResponse
from okta import UsersClient
from okta.models.user import User
from rest_framework import generics

from core.models import Config
from user.serializers import UserSerializer

from django.contrib.auth import get_user_model

config = Config()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            users_client = UsersClient(config.org_url, config.token)
            okta_user = User(login=serializer.data['email'],
                             email=serializer.data['email'],
                             firstName=serializer.data['first_name'],
                             lastName=serializer.data['last_name']
                             )
            try:
                okta_user_id = users_client.create_user(okta_user, activate=False).id
                if okta_user_id is not None:
                    user = get_user_model().objects.create_user(
                        email=serializer.data['email'],
                        first_name=serializer.data['first_name'],
                        last_name=serializer.data['last_name'],
                        okta_id=okta_user_id
                    )
                    return JsonResponse({"user_id": user.id}, status=201)

            except Exception as e:
                return e.args[0]

        return JsonResponse({"result": serializer.errors}, status=400)
