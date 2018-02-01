from django.shortcuts import render

def all_innovation_spaces(request):
    return render(
        request,
        'json',
    )

def singlefilter(request):
    return render(
        request,
        'json',
    )
