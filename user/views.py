from rest_framework import generics

from user.serializers import UserSerializer, AuthTokenSerializer
from okta_jwt.jwt import validate_token
from users.models import  Users
from users.serializers import CreateUserSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from okta.models.user import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from okta import UsersClient
from core.models import Config

config = Config()

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer



@swagger_auto_schema(method='post', request_body=CreateUserSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    access_token = request.META.get('HTTP_AUTHORIZATION')
    try:
        validate_token(access_token, config.issuer, config.aud, config.client_id)
    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": "token is invalid/null",
            "result": e.args[0]
        }, status=400)

    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        users_client = UsersClient(config.org_url, config.token)
        new_user = User(login=serializer.data['email'],
                        email=serializer.data['email'],
                        firstName=serializer.data['first_name'],
                        lastName=serializer.data['last_name'])
        try:
            user = users_client.create_user(new_user, activate=False)
            a_user = Users.objects.create(
                                          email=serializer.data['email'],
                                          first_name=serializer.data['first_name'],
                                          last_name=serializer.data['last_name'])
            a_user.save()

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "error on creating users",
                "result": e.args[0]
            }, status=400)

        return JsonResponse({
            "status": True,
            "message": "create user successfully",
            "result": {
                "user_id": a_user.id,
                "user_email": user.profile.email
            }
        }, status=200)

    return JsonResponse({
        "status": False,
        "message": "error on creating users",
        "result": serializer.errors
    }, status=400)
