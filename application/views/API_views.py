from django.shortcuts import render
from django.core import serializers
from application.serializers import SpaceSerializer
from application.models import Space
from django.http import HttpResponse,JsonResponse

def all_innovation_spaces(request):
	spaces = Space.objects.all()
	serializer = SpaceSerializer(spaces, many=True)
	return JsonResponse(serializer.data, safe=False)

def singlefilter(request):
    return render(
        request,
        'json',
    )
