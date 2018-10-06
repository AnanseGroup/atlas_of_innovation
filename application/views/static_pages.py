import json
from django.shortcuts import render
from django_countries import countries
from django.views.decorators.clickjacking import xframe_options_exempt

def map(request):
    type = ['All', 'Ecovillage', 'Event', 'Hub', 'Virtual', 'Workshop']
    theme = ['Agriculture', 'Appropriate Technology', 'Art and Culture', 'Biology', 'Design', 'Education', 'Food', 'Materials', 'Media', 'Politics', 'Science', 'Youth']
    filter = ['Type', 'Theme']
    context = {'type':type, 'theme':theme, 'filter':filter}
    return render(
        request,
        'makermap.html',
        context,
    )

@xframe_options_exempt
def whitelabel_map(request):
    filter_terms = request.GET.copy()
    context = {}
    map_center = filter_terms.pop('map_center', ["20,0"])[0].split(",")
    context['map_center'] = [float(map_center[0]), float(map_center[1])]
    context['map_zoom'] = int(filter_terms.pop('map_zoom', ["2"])[0])
    context['filter_terms'] = filter_terms.urlencode()
    return render(
        request,
        'whitelabel_map.html',
        context,
    )


def about(request):
    return render(
        request,
        'static/about.html',
    )


def goals(request):
    return render(
        request,
        'static/goals.html',
    )


def contributors(request):
    return render(
        request,
        'static/contributors.html',
    )


def userDocs(request):
    return render(
        request,
        'static/user-documentation.html',
    )


def devDocs(request):
    return render(
        request,
        'static/developer-documentation.html',
    )


def wiki(request):
    context = {'countries':countries}
    return render(
        request,
        'wiki.html',
        context,
    )


def contribute(request):
    return render(
        request,
        'static/contribute.html',
    )
