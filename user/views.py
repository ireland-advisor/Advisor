from django.http import JsonResponse
from okta import UsersClient
from okta.models.user import User
from rest_framework import generics, status
from core.models import Config
from user.serializers import UserSerializer

config = Config()


def create_okta_user(data):
    users_client = UsersClient(config.org_url, config.token)
    okta_user = User(login=data['email'],
                     email=data['email'],
                     firstName=data['first_name'],
                     lastName=data['last_name'],
                     password=data['password'])
    try:
        return users_client.create_user(okta_user, activate=False).id
    except Exception as e:
        raise e


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    # authentication_classes = (OktaAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                okta_user_id = create_okta_user(data)
                serializer.save(okta_id=okta_user_id)
                return JsonResponse({"result": {"okta_user_id": okta_user_id}},
                                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"result": {'error': e.args[0]}},
                                    status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"result": {'error': serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)