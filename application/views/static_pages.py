import json
from django.shortcuts import render


def home(request):
    return render(
        request,
        'makermap.html',
    )


def map(request):
    return render(
        request,
        'makermap.html',
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
    """
    with open('countries.json') as json_file:    
        data = json.load(json_file)
        c_list=[]
        for p in data['country']:
            c_list.append(p['countryName'])
        return {'countries':c_list}
    """
    return render(
        request,
        'wiki.html',
    )


def contribute(request):
    return render(
        request,
        'static/contribute.html',
    )
