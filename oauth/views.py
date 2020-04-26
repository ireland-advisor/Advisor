from django.http import JsonResponse, HttpResponse
from okta.models.user import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .serializer import CreateUserSerializer
from okta import UsersClient
from .models import Config

config = Config()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CreateUserSerializer(data=request.data)

    if serializer.is_valid():
        users_client = UsersClient(config.org_url, config.token)
        new_user = User(login=serializer.data['email'],
                        email=serializer.data['email'],
                        firstName=serializer.data['first_name'],
                        lastName=serializer.data['last_name'])
        try:
            users_client.create_user(new_user, activate=False)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "Error on creating users",
                "result": e.args[0]
            })

        return JsonResponse({
            "status": True,
            "message": "Create user successfully",
            "result": serializer.data
        })

    return JsonResponse({
        "status": False,
        "message": "Error on creating users",
        "result": serializer.errors
    })
