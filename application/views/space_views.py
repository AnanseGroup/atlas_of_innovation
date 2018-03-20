# These views render tempaltes that depend on the Atlas API, but they don't
# touch the database directly
from django.shortcuts import render
from application.models import Space
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def space_profile(request, id):
    space = Space.objects.get(id=id)
    return render(
        request,
        'space_profile.html',
        {"id": id, "space":space}
    )

class SpaceCreate(CreateView):
    model = Space
    template_name = 'space_edit.html'
    fields = '__all__'

add_space = SpaceCreate.as_view()

class SpaceEdit(UpdateView):
    model = Space
    template_name = 'space_edit.html'
    fields = '__all__'

edit_space = SpaceEdit.as_view()

class SpaceDelete(DeleteView):
    model = Space
    success_url = reverse_lazy("map")
    template_name = "space_confirm_delete.html"

delete_space = SpaceDelete.as_view()