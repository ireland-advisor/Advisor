from django.http import JsonResponse
from okta import UsersClient
from okta.models.user import User
from rest_framework import generics, status
from core.models import Config
from user.serializers import UserSerializer
from user.email_verify import send_email

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


def activate_okta_user(user_id):
    users_client = UsersClient(config.org_url, config.token)
    user = users_client.activate_user(user_id)
    if user is not None:
        return True
    else:
        return False


def send_verify_email(email, okta_user_id):
    send_email(email, okta_user_id)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                okta_user_id = create_okta_user(data)
                send_verify_email(data['email'], okta_user_id)
                serializer.save(okta_id=okta_user_id)
                return JsonResponse({"result": {"okta_user_id": okta_user_id}},
                                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"result": {'error': e.args[0]}},
                                    status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"result": {'error': serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)


class ActivateUser(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        okta_id = request.GET.get('okta_id')
        if okta_id is not None:
            activate_okta_user(okta_id)
            return JsonResponse({"result": "user activated"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"result": {'error': "user activate error"}},
                                status=status.HTTP_400_BAD_REQUEST)
