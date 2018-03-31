import json
from django.shortcuts import render
from django_countries import countries


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
