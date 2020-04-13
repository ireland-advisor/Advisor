# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from users.models import Mentor
from users.models import Seeker
from users.serializers import MentorSerializer, SeekerSerializer
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from users.serializers import UserSerializer, GroupSerializer
from django.http import QueryDict


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    @csrf_exempt
    def mentor_list(self, request):
        """
        List all code mentors, or create a new mentor.
        """
        if request.method == 'GET':
            mentors = Mentor.objects.all()
            serializer = MentorSerializer(mentors, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = MentorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    @csrf_exempt
    def mentor_detail(self, request, pk):
        """
        Retrieve, update or delete a code mentor.
        """
        try:
            mentor = Mentor.objects.get(pk=pk)
        except Mentor.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = MentorSerializer(mentor)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = MentorSerializer(mentor, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            mentor.delete()


class SeekerViewSet(viewsets.ModelViewSet):
    queryset = Seeker.objects.all()
    serializer_class = SeekerSerializer




    @csrf_exempt
    def seeker_list(self, request):
        """
        List all code seekers, or create a new seeker.
        """
        if request.method == 'GET':
            seekers = Seeker.objects.all()
            serializer = SeekerSerializer(seekers, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = SeekerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    @csrf_exempt
    def seeker_detail(self, request, pk):
        """
        Retrieve, update or delete a code seeker.
        """
        try:
            seeker = Seeker.objects.get(pk=pk)
        except Mentor.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = SeekerSerializer(seeker)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = SeekerSerializer(seeker, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            seeker.delete()
