from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import Http404

from application.models import Space
from application.models.spaces import SpaceForm
from application.models.spaces import DataCreditLog
import datetime

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
    
    def get_context_data(self, **kwargs):
        context = super(SpaceEdit, self).get_context_data(**kwargs)
        space = self.object
        ''' (Pedro) Part of #93 If space is validated we disallow accessing 
            the edit form I think a 404 error would suffice
        '''
        if space.validated:
            raise Http404
        return context

    def form_valid(self, form): 
        self.object = form.save()
        redirect_url = super(SpaceEdit, self).form_valid(form)

        ''' (Pedro) Related to #92 Add new anonymous credit to the credit log
        '''
        data_credit = {
                       'ip_address': self.request.META['REMOTE_ADDR'],
                       'space_id': self.object.id,
                       'credit': 'Anonymous'
                      }
        new_data_credit = DataCreditLog(**data_credit)
        new_data_credit.save()

        return redirect_url

edit_space = SpaceEdit.as_view()

class ListSpaces(TemplateView):
    template_name = "list.html"
list_spaces = ListSpaces.as_view()

# class DataCredit(TemplateView):
#      model = DataCreditLog
#      template_name ="history.html"
#      print("fffffffff")
#      def  data_credit_detail(request, id):
#         data_credit_log = DataCreditLog.objects.get(space_id=id)
#         print("basura"+data_credit_log)
# show_data_credit= DataCredit.as_view()

def show_data_credit(request, id):
        data_credit_log = (Space.objects.get(id=id))
        return render(
        request,
        'show_data_credit.html'        
    )