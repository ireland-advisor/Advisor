# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets
from django.http import JsonResponse


class AdvisorViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id'

    @csrf_exempt
    def advisor_list(self, request):
        if request.method == 'GET':
            advisors = Profile.objects.all()
            serializer = ProfileSerializer(advisors, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = ProfileSerializer(data=data)
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
            advisor = Profile.objects.get(user_id=pk)
        except Profile.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = ProfileSerializer(advisor)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = ProfileSerializer(advisor, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            advisor.delete()
