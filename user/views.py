from rest_framework import generics
from user.serializers import UserSerializer
from okta_jwt.jwt import validate_token
from django.http import JsonResponse
from okta.models.user import User
from okta import UsersClient
from core.models import Config

config = Config()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        access_token = request.META.get('HTTP_AUTHORIZATION')
        try:
            validate_token(access_token, config.issuer, config.aud, config.client_id)
        except Exception as e:
            return JsonResponse({"result": e.args[0]}, status=400)

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
                if user.id is not None:
                    return super().post(request)

            except Exception as e:
                return e.args[0]

        return JsonResponse({"result": serializer.errors}, status=400)
