from django.http import JsonResponse, HttpResponse
from okta.models.user import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .decorators import okta_login_required
from .serializer import CreateUserSerializer
from okta import UsersClient
from .models import Config, TokenManager, Advisor

config = Config()
token_manager = TokenManager()

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
            user = users_client.create_user(new_user, activate=False)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "error on creating users",
                "result": e.args[0]
            })
        return JsonResponse({
            "status": True,
            "message": "create user successfully",
            "result": {
                "user_id": user.id,
                "user_email": user.profile.email
            }
        })

    return JsonResponse({
        "status": False,
        "message": "error on creating users",
        "result": serializer.errors
    })


# @api_view(['POST'])
# @permission_classes([AllowAny])
# @okta_login_required
# def logout(request):
#     users_client = UsersClient(config.org_url, config.token)
#     user_id = request.POST["user_id"]
#     users_client.delete_user(user_id)
#     token_manager = None
#
#     return JsonResponse({"status": True,
#                          "message": "user delete successfully",
#                          })



