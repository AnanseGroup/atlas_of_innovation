# These views render tempaltes that depend on the Atlas API, but they don't
# touch the database directly
from django.shortcuts import render
from application.models import Space

def space_page(request, id):
    space = Space.objects.get(id=id)
    return render(
        request,
        'spacepage.html',
        {"id": id, "space":space}
    )

def edit_space(request):
    return render(
        request,
        'formedit.mako',
    )

