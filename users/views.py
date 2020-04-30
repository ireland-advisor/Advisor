# Create your views here.
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from users.models import Advisor, Users
from users.serializers import AdvisorSerializer, CreateUserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from okta.models.user import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from okta import UsersClient
from .models import Config

config = Config()


class AdvisorViewSet(viewsets.ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer

    @csrf_exempt
    def advisor_list(self, request):
        if request.method == 'GET':
            mentors = Advisor.objects.all()
            serializer = AdvisorSerializer(mentors, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = AdvisorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    @csrf_exempt
    def advisor_detail(self, request, pk):
        """
        Retrieve, update or delete a code mentor.
        """
        try:
            mentor = Advisor.objects.get(pk=pk)
        except Advisor.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = AdvisorSerializer(mentor)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = AdvisorSerializer(mentor, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            mentor.delete()


@swagger_auto_schema(method='post', request_body=CreateUserSerializer)
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
            Users.objects.create(okta_id=user.id,
                                 email=serializer.data['email'],
                                 first_name=serializer.data['first_name'],
                                 last_name=serializer.data['last_name']).save()

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
