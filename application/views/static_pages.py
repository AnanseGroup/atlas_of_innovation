import json
from django.shortcuts import render


def home(request):
    return render(
        request,
        'makermap.mako',
    )


def map(request):
    return render(
        request,
        'makermap.mako',
    )


def about(request):
    return render(
        request,
        'static/about.mako',
    )


def goals(request):
    return render(
        request,
        'static/goals.mako',
    )


def userDocs(request):
    return render(
        request,
        'static/user-documentation.mako',
    )


def devDocs(request):
    return render(
        request,
        'static/developer-documentation.mako',
    )


def wiki(request):
    with open('countries.json') as json_file:    
        data = json.load(json_file)
        c_list=[]
        for p in data['country']:
            c_list.append(p['countryName'])
        return {'countries':c_list}
    return render(
        request,
        'wiki.mako',
    )


def contribute(request):
    return render(
        request,
        'static/contribute.mako',
    )
