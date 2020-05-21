from django.http import JsonResponse
from rest_framework import generics, status
from user.okta_operations import create_okta_user, activate_okta_user
from user.serializers import UserSerializer
from user.email_verify import send_email


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                okta_user_id = create_okta_user(data)
                send_email(data['email'], okta_user_id)
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
            try:
                activated_okta_user_id = activate_okta_user(okta_id)
                return JsonResponse({"result": {"activated_user_id": activated_okta_user_id}},
                                    status=status.HTTP_200_OK)
            except Exception as e:
                return JsonResponse({"result": {'error': e.args[0]}},
                                    status=status.HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse({"result": {'error': "user activated error: okta_id is null"}},
                                status=status.HTTP_400_BAD_REQUEST)
