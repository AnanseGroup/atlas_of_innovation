from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from application.models import Space
from application.models.spaces import SpaceForm

def space_profile(request, id):
    space = Space.objects.get(id=id)
    return render(
        request,
        'space_profile.html',
        {"id": id, "space":space}
    )

class SpaceCreate(CreateView):
    form_class = SpaceForm
    model = Space
    template_name = 'space_edit.html'

add_space = SpaceCreate.as_view()

class SpaceEdit(UpdateView):
    form_class = SpaceForm
    model = Space
    template_name = 'space_edit.html'

edit_space = SpaceEdit.as_view()

class SpaceDelete(DeleteView):
    model = Space
    success_url = reverse_lazy("map")
    template_name = "space_confirm_delete.html"

delete_space = SpaceDelete.as_view()

class ListSpaces(TemplateView):
    template_name = "list.html"
list_spaces = ListSpaces.as_view()