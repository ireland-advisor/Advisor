from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import generics, status

from user.serializers import UserSerializer
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from core.decorators import okta_login_required


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    @method_decorator(okta_login_required)
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(
                email=serializer.data['email'],
                name=serializer.data['name'],
            )

            return JsonResponse({"user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
