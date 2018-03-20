# These views render the database as JSON 
from django.shortcuts import render
from django.core import serializers
from application.serializers import SpaceSerializer
from application.models import Space
from django.http import HttpResponse,JsonResponse

def all_innovation_spaces(request):
    spaces = Space.objects.all()
    serializer = SpaceSerializer(spaces, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_space(request, id):
    space = Space.objects.get(id=id)
    serializer = SpaceSerializer(space)
    return JsonResponse(serializer.data)

def change_space(request):
    return render(
        request,
        'static/thanks.mako',
    )

def add_space(request):
    return render(
        request,
        'static/thanks.mako',
    )

def delete_space(request):
    return render(
        request,
        'static/thanks.mako',
    )


