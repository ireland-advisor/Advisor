from django.utils.decorators import method_decorator
from rest_framework import generics
from user.serializers import UserSerializer
from django.http import JsonResponse
from okta.models.user import User
from okta import UsersClient
from core.models import Config
from django.contrib.auth import get_user_model
from core.decorators import okta_login_required

config = Config()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    @method_decorator(okta_login_required)
    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            users_client = UsersClient(config.org_url, config.token)
            new_user = User(login=serializer.data['email'],
                            email=serializer.data['email'],
                            firstName=serializer.data['name'],
                            lastName=serializer.data['name']
                            )
            try:
                user = users_client.create_user(new_user, activate=False)
                breakpoint()
                if user.id is not None:
                    advisor_user = get_user_model().objects.create_user(
                        email=serializer.data['email'],
                        name=serializer.data['name'],
                        okta_id=user.id
                    )
                    return JsonResponse({"result": {"user_id": advisor_user.id}}, status=200)

            except Exception as e:
                return e.args[0]

        return JsonResponse({"result": serializer.errors}, status=400)
