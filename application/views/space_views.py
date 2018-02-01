from django.shortcuts import render

def spacepage(request):
    return render(
        request,
        'wikipage.mako',
    )

def editspace(request):
    return render(
        request,
        'formedit.mako',
    )

def getspace(request):
    return render(
        request,
        'json',
    )

def change_space(request):
    return render(
        request,
        'static/thanks.mako',
    )

def singlefilterlist(request):
    return render(
        request,
        'list.mako',
    )
