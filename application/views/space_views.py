from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.contrib import messages


from django.http import Http404, HttpResponseRedirect
from django import forms


from django.http import Http404, HttpResponseRedirect
from django import forms

from application.models import Space, DataCreditLog
from application.models.spaces import SpaceForm,SpaceEditForm
from application.models.spaces import DataCreditLog
from django.forms.models import model_to_dict

from application.models import ProvisionalSpace
from application.models.space_multiselectfields import GovernanceOption, OwnershipOption, AffiliationOption
from django_countries import countries
from django.conf import settings as djangoSettings
from django.core.exceptions import ValidationError
import datetime
import csv
import tlsh
import itertools
import math
from django.db.models import Count
from application.serializers import SpaceSerializer
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.sites.shortcuts import get_current_site

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from post_office import mail
from application.views import mails
from application.models.user import Moderator,UserForm,MailResetPasswordForm,ResetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from application.models.user import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from django.forms.models import model_to_dict
from application.models.spaces import Suggestion
from application.models.spaces import FieldSuggestion
from application.models.spaces import Owners
from django import template
from application.decorators import user_is_autorized_in_Space,user_is_autorized_to_upload,user_is_autorized_to_analize

import ast
'''Shows profile of spaces '''
def space_profile(request, id):
    space = Space.objects.get(id=id)
    owners= Owners.objects.filter(space=space)
    if not owners:
       print(owners)
       owners = None
    if(request.method == 'POST'):
       #creating a new owner, the commented blok is for only create a suggestion
       # new_suggestion = CreateSuggestion(space,request.user)
       # CreateFieldSuggestion('owner',None,request.user,new_suggestion)
       # messages.success(request, 'Owner suggestion will be reviewed by administrator soon', extra_tags='alert')
       try:
        user=User.objects.get(id=request.POST.get('user_id'))
       except: 
        user= None
       if user == None:
          user=User.objects.filter(email=request.POST.get('user_email')).first()
       if user == None:
        messages.error(request, 'Error, user does not exist')
       else: 
        if IsOwner(user.id,id):
            messages.error(request, 'Error, user is already an owner of this space') 
        else:
            if IsModeratorOfSpace(request.user,space.province,space.country): # and user.moderator.country==space.country):
                CreateOwner(user,space)
                messages.success(request, 'Owner added correctly')
            else:
                # if(Owners.objects.filter(user=user).count()>=2):
                #   messages.error(request, 'You reached the limit of 2 owned spaces, contact the page moderator')
                # if user.moderator.country!=space.country:
                #    messages.error(request, 'You only can own a space in your country, contact the page moderator') 
                # messages.error(request, 'Owner not added')
                 new_suggestion = CreateSuggestion(space,request.user)
                 CreateFieldSuggestion('owner',None,request.user,new_suggestion)
                 messages.success(request, 'Owner suggestion will be reviewed by administrator soon', extra_tags='alert')

            return redirect('space_profile', id=id)
    return render(
        request,
        'space_profile.html',
        {"id": id, "space":space,"owners":owners}
    )


class SpaceCreate(LoginRequiredMixin, CreateView): 
    form_class = SpaceForm
    model = Space
    template_name = 'space_edit.html'
    login_url = '/login/'
    def form_valid(self, form):
                user=self.request.user
                redirect_url = redirect('contribute')
                affiliation_obj=None
                governance_obj=None
                ownership_obj=None
                if form.cleaned_data['network_affiliation']:
                    affiliation_obj = AffiliationOption.objects.filter(name=form.cleaned_data['network_affiliation']).first()

                if form.cleaned_data['governance_type']:
                    governance_obj = GovernanceOption.objects.filter(name=form.cleaned_data['governance_type']).first()
                    
                if form.cleaned_data['ownership_type']:
                    ownership_obj = OwnershipOption.objects.filter(name=form.cleaned_data['ownership_type']).first()
                
                new_space = ProvisionalSpace()

                for field in ProvisionalSpace._meta.get_fields():
                    if type(field).__name__ is not "ManyToManyField":
                        try:
                            form_field=form.cleaned_data[field.name]
                        except Exception:
                            form_field=None
                        if form_field is not None:
                            setattr(new_space,field.name,form.cleaned_data[field.name])
                    else:
                        try:
                            if ownership_obj:
                                new_space.ownership_type.add(ownership_obj)
                            if affiliation_obj:
                               new_space.network_affiliation.add(affiliation_obj)
                            if governance_obj:
                               new_space.governance_type.add(governance_obj)
                        except Exception:
                            print(Exception)
                new_space.override_analysis = False
                new_space.discarded = False
                if new_space.province:
                    new_space.province=new_space.province.strip().lower().capitalize()
                new_space.fhash = calculate_fhash(new_space)
                new_space.save() 
                new_space=ProvisionalSpace.objects.get(id=new_space.id)
                redirect_url=redirect('contribute')
                if not problemsPspace(self.request,new_space) and new_space.fhash:
                    if user.is_staff:
                        redirect_url = super(SpaceCreate, self).form_valid(form)
                        space = self.object
                        space.province=space.province.strip().lower().capitalize()
                        space.save()
                        messages.success(self.request, 'The space was created successfully', extra_tags='alert')
                        new_space.delete()
                        data_credit = {
                           'ip_address': self.request.META['REMOTE_ADDR'],
                           'space_id': space.id,
                           'credit': user.username

                        }
                        new_data_credit = DataCreditLog(**data_credit)
                        new_data_credit.save()
                    else:
                        messages.success(self.request, 'The space is valid, a moderator review and acept it soon', extra_tags='alert')
                        data_credit = {
                           'ip_address': self.request.META['REMOTE_ADDR'],
                           'space_id': new_space.id,
                           'credit': user.username,
                           'is_provisional':True,

                        }
                        new_data_credit = DataCreditLog(**data_credit)
                        new_data_credit.save()

                else:
                        messages.success(self.request, 'The space has problems, a moderator will get a notification to solve this problem', extra_tags='alert')
                        data_credit = {
                           'ip_address': self.request.META['REMOTE_ADDR'],
                           'space_id': new_space.id,
                           'credit': user.username,
                           'is_provisional':True,
                          }
                        new_data_credit = DataCreditLog(**data_credit)
                        new_data_credit.save()
                        moderators=GetModerators(new_space.province,new_space.country)
                        mails.on_create(new_data_credit, moderators)
                return redirect_url
add_space = SpaceCreate.as_view()



# class provisionalSpaceCreate(LoginRequiredMixin, CreateView): 
#     '''* **create a permanently space**'''
#     form_class = SpaceForm
#     model = provisionalSpace
#     template_name = 'space_edit.html'
#     login_url = '/admin/'
#     def form_valid(self, form):
#         '''* **if form data is valid create the new data credit whit username Save the space and credit log entry and finally if user isnt moderator or admin send mail to correspondent moderator**'''
#         space = self.object
        
#         user=self.request.user.username
#         self.object = form.save()
#         redirect_url = super(SpaceCreate, self).form_valid(form)

#         ''' (Pedro) Related to #92 Add new anonymous credit to the credit log
#         '''
#         data_credit = {
#                        'ip_address': self.request.META['REMOTE_ADDR'],
#                        'space_id': self.object.id,
#                        'credit': user

#                       }
#         new_data_credit = DataCreditLog(**data_credit)
#         space.fhash = calculate_fhash(space)
#         space.save()
#         new_data_credit.save()
#         messages.success(self.request, 'The space create success', extra_tags='alert')
#         if not self.request.user.is_staff:
#             try:
#                 moderators=Moderator.objects.filter(province=space.province)
#             except Exception :
#                 moderators=Moderator.objects.filter(country=space.country)
#             mails.on_create(new_data_credit, moderators)
#         return redirect_url

#     add_provisionalspace = provisionalSpaceCreate.as_view()
    

class SpaceEdit(LoginRequiredMixin, UpdateView):
    '''* **Edit a permanently space**'''
    form_class = SpaceEditForm
    model = Space
    template_name = 'space_edit.html'
    login_url = '/admin/'
   
    
    def get_context_data(self, **kwargs):
        '''* **(Pedro) Part of #93 If space is validated we disallow accessing he edit form I think a 404 error would suffice**'''
        context = super(SpaceEdit, self).get_context_data(**kwargs)
        space = self.object
        
        if space.validated:
            raise Http404
        return context
    def form_valid(self, form):
        if form.has_changed():   
            '''* **if form data is valid create the new data credit whit username Save the space and credit log entry and finally if user isnt moderator or admin send mail to correspondent moderator**'''
            space = self.object
            user=self.request.user.username
            data_credit = {
                               'ip_address': self.request.META['REMOTE_ADDR'],
                               'space_id': self.object.id,
                               'credit': user

                              }
            new_data_credit = DataCreditLog(**data_credit)
            if  self.request.user.is_superuser or IsOwner(self.request.user.id,space.id) or IsModeratorOfSpace(self.request.user,space.province,space.country):
                redirect_url = super(SpaceEdit, self).form_valid(form)
                #if is a administrator made changes
                
                
                
                self.object = form.save()
                

                ''' (Pedro) Related to #92 Add new anonymous credit to the credit log
                '''
                
                new_data_credit.save()
                messages.success(self.request, 'The space changes were successful', extra_tags='alert')
            else:#if is not an administrator then is just a suggestion
                redirect_url = redirect('contribute')
                # suggestion ={
                #             'space' : space,
                #             'user' :self.request.user
                #              }
                # new_suggestion= Suggestion(**suggestion)
                # new_suggestion.save()
                new_suggestion = CreateSuggestion(space,self.request.user)
                changed_fields=form.changed_data
                for field in changed_fields:
                            CreateFieldSuggestion(field,form,None,new_suggestion)
                moderators=GetOwners(space)
                if moderators is None:
                    moderators=GetModerators(space.province,space.country)         
                mails.on_change(new_data_credit, moderators)
                messages.success(self.request, 'The space suggestion will be evaluated by a moderator soon', extra_tags='alert')
        else:
            messages.error(self.request,'The form has not changed',extra_tags='alert')
        return redirect_url

            

edit_space = SpaceEdit.as_view()

class ListSpaces(TemplateView):
    '''* **list the spaces in the seleted country**'''
    template_name = "list.html"

list_spaces = ListSpaces.as_view()


@login_required
def show_data_credit(request, id):
        '''* **shows the historical changes credit for the selected space
        order by date in reverse order**'''
        data = DataCreditLog.objects.filter(space_id=id).exclude(is_provisional=True).order_by('-date')
        usernames = []
        for creditlog in data:
            try:
               name=User.objects.get(username=creditlog.credit).id
            except User.DoesNotExist:
                 name = None
            usernames.append(name)
        return render(
        request,
        'show_data_credit.html',
        {"data":data,"usernames":usernames,'id':id}     
    )
def get_userid(self,i):
        return self[i]

class UploadFileForm(forms.Form):
    '''**form to upload file**'''
    file = forms.FileField()

@staff_member_required
@user_is_autorized_to_analize
@ensure_csrf_cookie
def analyze_spaces(request):
    '''**first checks if exist the basic fields in the space if all exist then analize the spaces looking for coincidences,
     using the hashes, To simplify the process we just compare the provisional spaces with     
     their respective countries, so first we get all the countries available in our provisional list**'''
    gspaces = ProvisionalSpace.objects.values('country').annotate(
                                                        dcount=Count('country')
                                        ).order_by('country')
    country_list = []
    for gspace in gspaces:
        '''Don't know why but the query adds a None element to the dict'''
        if gspace['country'] is not None:
            country_list.append(gspace["country"])
    country_list.append(None)
    fields = ['latitude','longitude','name','city','website','email', 'fhash', 
              'postal_code', 'province', 'address1', 'id']
            
    '''To convert None to an empty string'''
    xstr = lambda s: '' if s is None else str(s)
    
    '''Spaces with no apparent problems'''
    approved_spaces = []
    
    '''Spaces without the required data to be analyzed'''
    excluded_spaces = []
    
    '''Spaces that match other spaces'''
    problem_spaces = []
    problem_spaces2 =[]#used for spaces match triguered by  distance
    ''' Discarded spaces'''
    discarded_spaces = []
    
    ''' Processed spaces'''
    processed_spaces = []
    if not request.user.is_superuser and (request.user.moderator.is_country_moderator or request.user.moderator.is_moderator):
        country_list=[request.user.moderator.country]
    permited_all_spaces_in_country= (request.user.is_superuser or request.user.moderator.is_country_moderator )
    
    for country in country_list:
        spaces = Space.objects.filter(country=country).all()

        if permited_all_spaces_in_country:
            pspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=False, discarded=False).all()
        else:
            pspaces = ProvisionalSpace.objects.filter(country=country,province=request.user.moderator.province, override_analysis=False, discarded=False).all()
           

        ''' (Pedro) The list that will hold the id of the spaces we need to 
            filter so they won't go to the approved list '''
        pop_list = []
        
        ''' First we analyze each space for problems in the data 
        '''
        for pspace in pspaces:
            problems = [] 
            critical = 0
            error = 0 
            ''' (Pedro) added the critical flag thinking maybe in the future some
                of this problems aren't really critical '''
            if not pspace.address1:
                problems.append({"desc":"Space has no main address", "crit":1})
                critical = 1
                error = 1 
            if not pspace.city:
                problems.append({"desc":"Space has no city", "crit":1})
                critical = 1
                error = 1
            if not pspace.province:
                problems.append({"desc":"Space has no province", "crit":1})
                critical = 1
                error = 1
            if not pspace.email:
                problems.append({"desc":"Space has no contact email", "crit":1})
                critical = 1
                error = 1
            if not pspace.website:
                problems.append({"desc":"Space has no website", "crit":1})
                critical = 1
                error = 1
            if not pspace.fhash:
                problems.append({"desc": "Space has no hash: see note at header", "crit":1})
                critical = 1
                error = 1
            if not pspace.country:
                problems.append({"desc": "Space has no country", "crit":1})
                critical = 1
                error = 1
            if critical:
                pop_list.append(pspace.id)
            if error:
                excluded_spaces.append([model_to_dict(pspace,fields=fields), problems]) 

        ''' Provisional spaces with critical errors cant be added to the match 
            comparison so we filter those spaces '''
        if permited_all_spaces_in_country:
           pspaces = ProvisionalSpace.objects.filter(
                                                 country=country,
                                                 override_analysis=False,
                                                 discarded=False
                                             ).exclude(
                                                 id__in=pop_list
                                             ).all()
        else:  
            pspaces = ProvisionalSpace.objects.filter(
                                                 country=country,
                                                 province=request.user.moderator.province,
                                                 override_analysis=False,
                                                 discarded=False
                                             ).exclude(
                                                 id__in=pop_list
                                             ).all()

        if spaces:
            for a, b in itertools.product(spaces, pspaces):
               if a.fhash: 
                try:
                    num = tlsh.diffxlen(a.fhash, b.fhash)

                    if num<5:
                        b.override_analysis=False
                        b.discarded=True
                        b.save();
                        problem_spaces=[x for x in problem_spaces if x[1]['id']!=b.id]
                        pop_list.append(b.id)
                    else:
                      if num < 100: 
                            ''' If we find a match we add
                            problem list'''
                        
                            problem_spaces.append([model_to_dict(a,fields=fields),
                                               model_to_dict(b,fields=fields),
                                               num])

                            pop_list.append(b.id)
                      else:
                          num1=abs(a.latitude-b.latitude)
                          num2=abs(a.longitude-b.longitude)

                          if num1<.003 and num2 <abs(.0053*math.cos(num1)):
                                    #if not b.override_analysis and not b.discarded:#can be discarted in perfect match
                                    problem_spaces2.append([model_to_dict(a,fields=fields),
                                                       model_to_dict(b,fields=fields),
                                                       num])

                                    pop_list.append(b.id)
                                    print('distance')      

                     
                except:
                    '''There are many ways this can make an exception for once
                    the spaces may not have a fhash because is missing data so
                    we take a look
                    '''
                    pass
               else:
                try:
                  
                    num1=abs(a.latitude-b.latitude)
                    num2=abs(a.longitude-b.longitude)

                    if num1<.003 and num2 <abs(.0053*math.cos(num1)):
                                #if not b.override_analysis and not b.discarded:#can be discarted in perfect match
                                problem_spaces2.append([model_to_dict(a,fields=fields),
                                                   model_to_dict(b,fields=fields),
                                                   num])

                                pop_list.append(b.id)
                                print('distance')
                except:
                    '''There are many ways this can make an exception for once
                    the spaces may not have a fhash because is missing data so
                    we take a look
                    '''
                    pass

            '''We filter the spaces yet again so the ones with a match problem 
            don't make the approved list'''

            if permited_all_spaces_in_country:
                pspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=False, discarded=False).exclude(id__in=pop_list).all()
            else:
                pspaces = ProvisionalSpace.objects.filter(country=country,province=request.user.moderator.province, override_analysis=False, discarded=False).exclude(id__in=pop_list).all()
            
            approved_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in pspaces])
        else:
            ''' If there are no spaces to compare we add all provision spaces
            to the approved list (yay?)'''
            approved_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in pspaces])

        # Lets add the discarded spaces
        for space in problem_spaces2:
            problem_spaces.append(space)
        problem_spaces2=[]
        print(problem_spaces)
        problem_spaces.sort(key=lambda pspace: pspace[0]['id'])
        if permited_all_spaces_in_country:
           dspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=False, discarded=True).all()
        else:
            dspaces = ProvisionalSpace.objects.filter(country=country,province=request.user.moderator.province, override_analysis=False, discarded=True).all() 
            if dspaces is None:
               dspaces = ProvisionalSpace.objects.filter(country=country,province=request.user.moderator.province, override_analysis=False, discarded=True).all()  
        discarded_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in dspaces])

        # Lets add the processed spaces
        if permited_all_spaces_in_country:
           pspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=True, discarded=False).all()
        else:
            pspaces = ProvisionalSpace.objects.filter(country=country,province=request.user.moderator.province, override_analysis=True, discarded=False).all()
        processed_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in pspaces])
    analized_spaces=[]
    for pspace in discarded_spaces:
        #print(pspace['id'],'discarted')
        analized_spaces.append(pspace['id'])
    for pspace in processed_spaces:
        #print(pspace['id'],'processed_spaces')
        analized_spaces.append(pspace['id'])
    for pspace in approved_spaces:
        #print(pspace['id'],'aproved')
        analized_spaces.append(pspace['id'])
    for pspace in problem_spaces:
        #print(pspace[1]['id'],'problem')
        analized_spaces.append(pspace[1]['id'])
    for pspace in excluded_spaces:
        #print(pspace[0]['id'],'excluded')
        analized_spaces.append(pspace[0]['id'])
            
    
    if request.user.is_superuser:
        country_error_spaces=ProvisionalSpace.objects.all().exclude(id__in=analized_spaces)

    else:
        if permited_all_spaces_in_country:
           country_error_spaces=ProvisionalSpace.objects.filter(country=request.user.moderator.country).exclude(id__in=analized_spaces)
        else:
            country_error_spaces=ProvisionalSpace.objects.filter(country=request.user.moderator.country).filter(province=request.user.moderator.province).exclude(id__in=analized_spaces)
    problems=[]
    problems.append({"desc": "Space has country errors", "crit":1})
    for pspace in country_error_spaces:
        excluded_spaces.append([model_to_dict(pspace,fields=fields), problems]) 
    

    data = request.GET.copy()
    discarded_id=[]
    processed_id=[]
    for pspaces in discarded_spaces:
        discarded_id.append({'id' : pspaces['id']})
    for pspaces in processed_spaces:
        processed_id.append({'id' : pspaces['id']})
    if data and data.get("json_list"):
        return JsonResponse({'approved': approved_spaces,
                             'problem': problem_spaces,
                             'excluded': excluded_spaces,
                             'discarded_id': discarded_id,
                              'processed_id':processed_id
                            })
    else:
        
        return render(request, 'space_analysis.html', {'approved': approved_spaces, 
                                                   'problem': problem_spaces,
                                                   'excluded': excluded_spaces,
                                                   'discarded': discarded_spaces,
                                                   'processed': processed_spaces,
                                                   'discarded_id': discarded_id,
                                                   'processed_id':processed_id,
                                                   'problem2': problem_spaces2
                                                   })

def problemsPspace(request,pspace):
            spaces = Space.objects.all()
            problems = [] 
            nohash =[]
            critical = 0
            error = 0 
            ''' (Pedro) added the critical flag thinking maybe in the future some
                of this problems aren't really critical '''
            if not pspace.address1:
                problems.append({"desc":"Space has no main address", "crit":1})
                critical = 1
                error = 1 
            if not pspace.city:
                problems.append({"desc":"Space has no city", "crit":1})
                critical = 1
                error = 1
            if not pspace.province:
                problems.append({"desc":"Space has no province", "crit":1})
                critical = 1
                error = 1
            if not pspace.email:
                problems.append({"desc":"Space has no contact email", "crit":1})
                critical = 1
                error = 1
            if not pspace.website:
                problems.append({"desc":"Space has no website", "crit":1})
                critical = 1
                error = 1
            if not pspace.fhash:
                problems.append({"desc": "need bee reviewed by admin", "crit":1})
                print('pspace.fhash',pspace.fhash)
                critical = 1
                error = 1
            if not pspace.country:
                problems.append({"desc": "Space has no country", "crit":1})
                critical = 1
                error = 1
            ''' Provisional spaces with critical errors cant be added to the match 
            comparison so we filter those spaces '''
            if spaces:
            
             for a, b in itertools.product(spaces, [pspace]):
                
              if a.fhash:
                    
                
                try:
                    num = tlsh.diffxlen(a.fhash, b.fhash)

                    
                    if num<5:
                        b.override_analysis=False
                        b.discarded=True
                        b.save(); 
                        problems.append({"desc":"Space already exists in the data base","crit":1})  
                    else:
                        if num < 80: 
                            print('match')
                            ''' If we find a match we add those spaces to our 
                                problem list'''
                            problems.append({"desc":"A similar space already exist in the data base","crit":1})
                        else:
                            if num < 100:
                                problems.append({"desc":"Space may be a duplicate, contact the page moderator","crit":1})

                except:
                    '''There are many ways this can make an exception for once
                    the spaces may not have a fhash because is missing data so
                    we take a look
                    '''
                    pass
              else:
                
                try:
                    num1=abs(a.latitude-b.latitude)
                    num2=abs(a.longitude-b.longitude)
                except:
                    num1=1
                if num1<.003 and num2 <abs(.0053*math.cos(num1)):#rectangle of 666.666m per side
                    print('distance match')
                    problems.append({"desc":"space has one posible coincidence  whit a space","crit":1})
               

            if problems:
                for problem in problems:
                    messages.success(request, 'The space has a problem:'+ problem['desc'], extra_tags='alert')
                print('1')    
                return 1
            print('0') 
            return 0
            '''We filter the spaces yet again so the ones with a match problem 
            don't make the approved list'''
            

@staff_member_required
@user_is_autorized_to_upload
def upload_file(request):
    '''* **check if the fileselected for upload  is valid**'''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            handle_csv(request,request.FILES['file'])

            return HttpResponseRedirect('/analyze/provisional_spaces/')
    else:
        form = UploadFileForm()
    return render(request, 'space_upload.html', {'form': form})


def handle_csv(request,file):


        '''**process the spaces in the file uploaded,
        applying the nesesary changes to ensure the new spaces have the correct format and can be 
        saved as provisional spaces to analize it**'''
        send_to_default_moderator=0


        data_filename = file

        reverse_country_list = {name:code for code, name in countries}
        reverse_country_list2 = {code:name for code, name in countries}
        with open(djangoSettings.BASE_DIR+'/temp.csv', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        ProvisionalSpace.objects.all().delete()
        with open(djangoSettings.BASE_DIR+"/temp.csv", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            # replace empty strings with None

            try:
                complete_spaces = [{key: value if not value == '' else None \
                                for key, value in row.items()} for row in reader]
            except:
                messages.error(request, 'The file has an error, to fix it, you can open it in free office and save it as "Use Text CSV Format"', extra_tags='alert')
                complete_spaces = []

            processed_spaces = []
            contacted_moderators=[]
            for space in complete_spaces:
                processed_space = {}
                
                # Some spaces may not have a name for a reason or other ¯\_(ツ)_/¯
                processed_space["name"] = space.pop('name', "Untitled")
                if processed_space["name"] == None or processed_space["name"].strip() == "":
                    processed_space["name"] = "Untitled" 

                # Fields that can be named other things
                processed_space['address1'] = space.pop('street_address', None)
                space_country_name = space.pop('country', None)
                if space_country_name in reverse_country_list:
                    processed_space['country'] = reverse_country_list[space_country_name]
                elif space_country_name in reverse_country_list2:
                    space_country_name=reverse_country_list[space_country_name2]
                    processed_space['country'] = reverse_country_list[space_country_name]
                elif space_country_name == "United States":
                    processed_space['country'] = \
                                    reverse_country_list['United States of America']
                else: # if the country name isn't in the dictionary:
                    # put the country name back in the unvalidated space
                    space['country'] = space_country_name
                processed_space['website'] = space.pop('primary_website', None)
                processed_space['province'] = space.pop('state', None)
                if processed_space['province']:
                    processed_space['province'] = processed_space['province'].strip()
                    processed_space['province'] = processed_space['province'].lower().capitalize()
                    print(processed_space['province'])
                processed_space['data_credit'] = space.pop('source', None)
                processed_space['date_opened'] = space.pop('date_of_founding', None)
                if processed_space['date_opened']:
                    try:
                        month, day, year = processed_space['date_opened'].split("/")
                        processed_space['date_opened'] = datetime.date(month=int(month), \
                                                                    day=int(day), \
                                                                    year=int(year))
                    except ValueError:
                        pass
                activity_level = space.pop('status', None)
                if activity_level == 'active' or activity_level == 'Active':
                    processed_space['operational_status'] = "In Operation"
                elif activity_level == 'planned' or activity_level == 'Planned':
                    processed_space['operational_status'] = "Planned"
                elif activity_level == 'inactive':
                    processed_space['operational_status'] = "Closed"
                    
                ''' (PEDRO) Related to #93 I imagine the CSV to import may
                    have a trusted_source field or at least a validation_status
                    field with the corresponding option
                '''
                trusted_source = space.pop('trusted_source', False)
                if trusted_source:
                    processed_space['validation_status'] = 'Verified'
                    
                validation_status = space.pop('validation_status', None)
                if validation_status:
                    processed_space['validation_status'] = validation_status
                
                
                # Gets the affiliation ManyToMany option 
                affiliation = space.pop('network_affiliation', None)
                affiliation_obj = None
                if affiliation:
                    affiliation_obj = AffiliationOption.objects.filter(name=affiliation).first()

                # Gets the governance ManyToMany option 
                governance = space.pop('governance', None)
                governance_obj = None
                if governance:
                    governance_obj = GovernanceOption.objects.filter(name=governance).first()
                    
                # Gets the ownership ManyToMany option 
                ownership = space.pop('ownership', None)
                ownership_obj = None
                if ownership:
                    ownership_obj = OwnershipOption.objects.filter(name=ownership).first()
                
                # Fields that share the name of where they are going
                for field in ProvisionalSpace._meta.get_fields():
                    if not field.name in processed_space:
                        # (PEDRO) To solve #85 remove the many to many fields
                        if type(field).__name__ is not "ManyToManyField":
                            processed_space[field.name]=space.pop(field.name, None)
                space = {field:space[field] for field in space if space[field]}
                processed_space['other_data'] = space
                #processed_spaces.append(processed_space)
                
                '''(Pedro) Removed the for loop, there may be a performance hit
                    but I did it to add the ManyToMany relationships'''
                new_space = ProvisionalSpace(**processed_space)
                new_space.override_analysis = False
                new_space.discarded = False
                try:
                    new_space.clean_fields()
                except ValidationError as v:
                    for field in v.error_dict:
                        new_space.other_data[field] = new_space.__dict__[field]
                        setattr(new_space, field, None)
                try:
                    new_space.fhash = calculate_fhash(new_space)
                    new_space.save()
                    ''' Added the many to many relationship'''
                    if ownership_obj:
                        new_space.ownership_type.add(ownership_obj)
                    if affiliation_obj:
                        new_space.network_affiliation.add(affiliation_obj)
                    if governance_obj:
                        new_space.governance_type.add(governance_obj)
                    new_space.save() 
                    data_credit = {
                           'ip_address': request.META['REMOTE_ADDR'],
                           'space_id': new_space.id,
                           'credit': request.user.first_name

                          }
                    new_data_credit = DataCreditLog(**data_credit)
                    new_data_credit.is_provisional=True
                    new_data_credit.save()
                    moderators=GetModerators(new_space.province,new_space.country) 
                    if moderators is not None:
                        for moderator in moderators:
                            if not ( moderator in contacted_moderators):
                                print(moderator)
                                contacted_moderators.append(moderator)
                                if not moderator.user==request.user:
                                    mails.on_create(new_data_credit,[moderator])
                                    print(moderator)
                    else:
                        if not send_to_default_moderator:
                            mails.on_create(new_data_credit,moderators)
                            send_to_default_moderator=1
                except Exception as e:
                    
                    raise e
                    
def calculate_fhash(new_space):
    '''**concatenate the name , address city province country and postal code if they exist,
    then calculate the tlsh hash  and return it**'''
    space_info = [new_space.name]
    if new_space.address1:
        space_info.append(new_space.address1)
    if new_space.city:
        space_info.append(new_space.city)
    if new_space.province:
        space_info.append(new_space.province)
    if new_space.country:
        space_info.append(str(new_space.country))
    if new_space.postal_code:
        space_info.append(new_space.postal_code)
    space_stuff = " ".join(space_info).replace(",", "").replace("-","").replace(".","").replace("_","").replace("+","")
    space_string = ' '.join(space_stuff.split()).encode("raw_unicode_escape")
    print(len(space_stuff))
    return tlsh.forcehash(space_string)

@staff_member_required
@user_is_autorized_to_analize
def provisional_space(request):
    '''* **provides the  way to show and  modify the provisional spaces stored in the db**'''
    fields = ['latitude','longitude','name','city','country','website', 'postal_code','email', 'province', 'address1', 'id']
    if request.method == 'GET':

        if request.GET["id"]:
            id = request.GET["id"]
            space = ProvisionalSpace.objects.filter(id=id).first()
            serializer = SpaceSerializer(space, fields=fields, many=False)
            return JsonResponse(serializer.data, safe=False)
        else: 
            # TODO Return 404
            pass
    if request.method == 'POST':
        data = request.POST.copy()
        id = data.pop('id')
        print(id)
        space = ProvisionalSpace.objects.filter(id=id[0]).first()

        if space:
            for key, value in data.items():
                if value:
                  setattr(space,key,value)
                  print(key,value)
            space.fhash = calculate_fhash(space)
            space.save()

        return JsonResponse({'success':1})
    if request.method == "PUT":


        spaces_list=[]


        if(isinstance(request.body,(bytes, bytearray))):
            str_response = request.body.decode('utf-8')
            data = json.loads(str_response)
        else:
            data = json.loads(request.body)


        if data and data['id']:
            spaces = ProvisionalSpace.objects.filter(id__in=data['id']).all()
            
            for space in spaces:
                if space and data.get('override_analysis'):
                    space.override_analysis = True
                    space.discarded = False
                if space and data.get('discarded'):
                    space.discarded = True
                    space.override_analysis = False
                if space and data.get('reset_flags'):
                    space.discarded = False
                    space.override_analysis = False
                space.save()
                serializer = SpaceSerializer(space, fields=fields, many=False)
                spaces_list.append(serializer.data)               
        return JsonResponse(spaces_list, safe=False)
    if request.method == "DELETE":
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            data = None
        
        if data is None:
           spaces = ProvisionalSpace.objects.filter(discarded=True).delete()
           print('all')
        else:
           print('by id')
           if isinstance(data,str):
              data=ast.literal_eval(data)
              for id in data:
                 spaces = ProvisionalSpace.objects.filter(id=id['id']).delete()
           else:
                spaces = ProvisionalSpace.objects.filter(id__in=data['id']).delete()
        return JsonResponse({'success':1}, safe=False)
    if request.method == "PATCH":
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            data = None
        spaces=[]
        if data is None:
            spaces = ProvisionalSpace.objects.filter(override_analysis=True).all()
        else:
            
            if isinstance(data,str):
              data=ast.literal_eval(data)
              
              for id in data:
                try:
                    
                  spaces.append(ProvisionalSpace.objects.get(id=id['id']))
                except Exception:
                            
                            print(Exception)
                            
            else:
                spaces.append(ProvisionalSpace.objects.get(id__in=data['id']))
            
        for space in spaces:
            new_space = Space()
            for field in space._meta.fields:
                if field.name not in ["id", "discarded", "override_analysis"]:
                    setattr(new_space, field.name, getattr(space, field.name))
            new_space.save()
            '''adding creditlog if exist for this provisional spaces'''
            credits=DataCreditLog.objects.filter(space_id=space.id).exclude(is_provisional=False)
            print(credits)
            for credit in credits:
                credit.space_id=new_space.id
                credit.is_provisional=False
                credit.save()
            space.delete()
            
        return JsonResponse({'success':1}, safe=False)

@staff_member_required
def space_csv(request):
    '''* ***Used to show analize the spaces in the database(not provisional spaces) and calculate the hash if it doesn exist**'''

    fields = ['latitude','longitude','name','city','country','website', 'postal_code','email', 'province', 'address1', 'id']
    if request.method == 'GET':
        if request.GET["id"]:
            id = request.GET["id"]
            space = Space.objects.filter(id=id).first()
            serializer = SpaceSerializer(space, fields=fields, many=False)
            return JsonResponse(serializer.data, safe=False)
        else:
            # TODO Return 404
            pass
    if request.method == 'POST':
        data = request.POST.copy() 
        id = data.pop('id') 
        print(id)
        print(id[0])
        space = Space.objects.filter(id=id[0]).first()
        if space:
            for key, value in data.items():
                setattr(space,key,value)
            space.fhash = calculate_fhash(space) 
            space.save()
        return JsonResponse({'success':1})


def signup(request):
    '''**allow to create an acount as basic user , the new account must be verified by email 
    when it perform any change  o create a new space a email is send to correspondent moderator to validate the changes**'''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Moderator.objects.create(user=user)
            user.moderator.country=form.cleaned_data['country']
            user.moderator.save()
            mail.send(
                    [form.cleaned_data.get('email')], # List of email addresses also accepted
                    'noreply@atlasofinnovation.com',
                    subject='Activate Your Atlas Account',
                    priority='now',
                    message=render_to_string('account_activation_email.html', {
                        'user': user,
                        'domain': djangoSettings.URL,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user),
                    }),
                    
                    )
            messages.info(request, 'The activation mail was sent')
            return redirect('/contribute')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    '''* **Activate the account when the user acces to link provide in the mail**'''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.moderator.email_confirmed = True
        user.save()
        login(request, user)
        messages.info(request, 'Welcome to Atlas of Innovation, your account was activated successfully!')
        return redirect('home')
    else:
        messages.info(request, 'The page does not exist!')
        return redirect('/')

def password_reset(request):
    '''**allow to create an acount as basic user , the new account must be verified by email 
    when it perform any change  o create a new space a email is send to correspondent moderator to validate the changes**'''
    if request.method == 'POST':
        form = MailResetPasswordForm(request.POST)
        if form.is_valid():
            print("is valid")
            try:
                user=User.objects.get(email=form.cleaned_data.get('email'))
            except:
                user=None
            print(user)
            if(user is not None):
                mail.send(
                        [form.cleaned_data.get('email')], # List of email addresses also accepted
                        'noreply@atlasofinnovation.com',
                        subject='Reset your Atlas Password',
                        priority='now',
                        message=render_to_string('reset_password_email.html', {
                            'user': user,
                            'domain': djangoSettings.URL,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                            'token': account_activation_token.make_token(user),
                        }),
                        
                        )
                messages.info(request, 'The reset password mail was sent!')
            else:
                messages.info(request, 'The email does not exist in db!')
                return redirect('/reset_password')
            return redirect('/contribute')
    else:
        form = MailResetPasswordForm()
    return render(request, 'password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    '''* **Activate the account when the user acces to link provide in the mail**'''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if request.method == 'GET':
        form = ResetPasswordForm()
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'password_reset_confirm.html', {'form': form})
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if( form.is_valid):
            print(form['password'].value())
            if(form['password'].value()==form['confirm_password'].value()):
                user.set_password(form['password'].value())


                user.save()
                login(request, user)
                messages.info(request, 'Password resetted successfully!')
                return redirect('/')
            else:
                messages.info(request,'Passwords do not match!')
                print('/'+request.path_info)
                return HttpResponseRedirect(request.path_info)
    
    messages.info(request, 'The page does not exist!')
    return redirect('/')


def login_user(request, template_name='registration/login.html', extra_context=None):
     response = auth_views.login(request, template_name)
     if request.POST.has_key('remember_me'):
        request.session.set_expiry(1209600) # 2 weeks
@user_is_autorized_in_Space
def Suggestions(request,space_id):
        data = Suggestion.objects.filter(space=space_id).filter(active=True).order_by('-date')
        fields=[]
        for suggest in data:
            fields.append(FieldSuggestion.objects.filter(suggestion=suggest))
        return render(
        request,
        'suggest.html',
        {"id": space_id, "data":data,"fields":fields}
    )
@login_required
def Discart_suggestion(request,suggestion_id):
    Suggestion.objects.filter(id=suggestion_id).update(active=False)
    messages.info(request, 'The suggested change was discarded!')
    return redirect(request.GET.get('next'))
@login_required
def Acept_suggestion(request,pk,suggestion_id):
    fields=FieldSuggestion.objects.filter(suggestion=suggestion_id)
    for field in fields:
        if field.field_name !='owner':
            type1=Space._meta.get_field(field.field_name).get_internal_type()
            if type1 is not "ManyToManyField":
                Space.objects.filter(id=pk).update(**{field.field_name:field.field_suggestion})
            else:   
                    space=Space.objects.get(id=pk)
                    if field.field_name == 'network_affiliation':
                        obj = AffiliationOption.objects.filter(name=field.field_suggestion).first()
                        space.network_affiliation.add(obj)
                    else:
                        if field.field_name == 'governance_type':
                           obj = GovernanceOption.objects.filter(name=field.field_suggestion).first()
                           space.governance_type.add(obj)
                        else:
                            if field.field_name =='ownership_type':
                               obj = OwnershipOption.objects.filter(name=field.field_suggestion).first()
                               space.ownership_type.add(obj)
        else:
            CreateOwner(Suggestion.objects.get(id=suggestion_id).user,Space.objects.get(id=pk))           
    Suggestion.objects.filter(id=suggestion_id).update(active=False)
    data_credit = {
                               'ip_address': request.META['REMOTE_ADDR'],
                               'space_id': pk,
                               'credit': Suggestion.objects.get(id=suggestion_id).user.username

                              }
    new_data_credit = DataCreditLog(**data_credit)
    new_data_credit.save()
    messages.info(request, 'The Space was updated!')
    return redirect(request.GET.get('next'))

@staff_member_required
def AllSuggestion(request):
        suggestions = Suggestion.objects.filter(active=True).distinct("space").all()

        data=[]
        for suggestion in suggestions:
            data.append(suggestion.space)
        print(data)

        return render(
        request,
        'all_suggestion.html',
        { "data":data}
    )

def CreateSuggestion(space,user):
    suggestion ={
                            'space' : space,
                            'user' :user
                             }
    new_suggestion= Suggestion(**suggestion)
    new_suggestion.save()
    return  new_suggestion

def CreateFieldSuggestion(field,form,data,suggestion):
    if field not in ["id","captcha"]:
        if form is not None:
                            if Space._meta.get_field(field).get_internal_type() is not "ManyToManyField":
                                field_suggest = {
                                              'field_name': field,
                                              'field_suggestion':form.cleaned_data[field]
                                                 }
                            else:
                                field_suggest = {
                                              'field_name': field,
                                              'field_suggestion':form.cleaned_data[field].first().name
                                                 }
        else:
            field_suggest = {
                                              'field_name': field,
                                              'field_suggestion':data
                                                 }
        new_field_suggestion = FieldSuggestion(**field_suggest)
        print(new_field_suggestion)
        new_field_suggestion.suggestion=suggestion
        new_field_suggestion.save()

def CreateOwner(user,space):
            owner={
                    'user':user,
                    'space':space
            }
            new_owner=Owners(**owner)
            new_owner.save()
#if user is owner of the provide space return true
def IsOwner(user_id,space_id):
            owners = Owners.objects.filter(space=space_id,user=user_id)
            if owners.count()>0:
                return True
            return False
def IsModeratorOfSpace(user,province,country):
                if user.is_superuser:
                    return True
                if user.moderator.is_moderator:
                    if province is not None and user.moderator.province is not None and user.moderator.province == province:
                        return True
                if user.moderator.is_country_moderator:
                    if user.moderator.country == country:
                        return True
                return False  

@staff_member_required
def DeleteOwner(request,space,user):
    Owners.objects.filter(space=space,user=user).delete()
    messages.success(request, 'owner deleted')
    return redirect(request.GET.get('next'))
def GetModerators(province,country):
                moderators=None
                if province is not None:
                    moderators=Moderator.objects.filter(country=country,province=province,is_moderator=True)

                if moderators is not None and moderators.count() == 0: 
                    moderators=Moderator.objects.filter(country=country,is_country_moderator=True)
                print(moderators)
                return moderators
def GetOwners(space_id):
    owners=Owners.objects.filter(space=space_id)
    if owners.count() == 0:
        return None
    users=[]
    for owner in owners:
        try:
         users.append(owner.user.moderator)
        except:
         print("no moderator")
    print(users)
    return users