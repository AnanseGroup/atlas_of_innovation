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

from application.models import Space, DataCreditLog
from application.models.spaces import SpaceForm
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

from django.db.models import Count
from application.serializers import SpaceSerializer
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required

def space_profile(request, id):
    space = Space.objects.get(id=id)
    return render(
        request,
        'space_profile.html',
        {"id": id, "space":space}
    )

 
class SpaceCreate(LoginRequiredMixin, CreateView):
    form_class = SpaceForm
    model = Space
    template_name = 'space_edit.html'
    login_url = '/admin/'

add_space = SpaceCreate.as_view()
 
class SpaceEdit(LoginRequiredMixin, UpdateView):
    form_class = SpaceForm
    model = Space
    template_name = 'space_edit.html'
    login_url = '/admin/'
    
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

class UploadFileForm(forms.Form):
    file = forms.FileField()

@staff_member_required
@ensure_csrf_cookie
def analyze_spaces(request):

    ''' To simplify the process we just compare the provisional spaces with 
    their respective countries, so first we get all the countries available in
    our provisional list'''
    gspaces = ProvisionalSpace.objects.values('country').annotate(
                                                        dcount=Count('country')
                                        ).order_by('country')
    country_list = []
    for gspace in gspaces:
        # Don't know why but the query adds a None element to the dict
        if gspace['country'] is not None:
            country_list.append(gspace["country"])

    fields = ['latitude','longitude','name','city','website','email', 'fhash', 
              'postal_code', 'province', 'address1', 'id']
            
    # To convert None to an empty string
    xstr = lambda s: '' if s is None else str(s)
    
    # Spaces with no apparent problems
    approved_spaces = []
    
    # Spaces without the required data to be analyzed
    excluded_spaces = []
    
    # Spaces that match other spaces
    problem_spaces = []
    
    # Discarded spaces
    discarded_spaces = []
    
    # Processed spaces
    processed_spaces = []
    
    for country in country_list:
        spaces = Space.objects.filter(country=country).all()
        pspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=False, discarded=False).all()
        print(len(pspaces))
        
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
            if critical:
                pop_list.append(pspace.id)
            if error:
                excluded_spaces.append([model_to_dict(pspace,fields=fields), problems]) 

        ''' Provisional spaces with critical errors cant be added to the match 
            comparison so we filter those spaces '''
        pspaces = ProvisionalSpace.objects.filter(
                                                 country=country,
                                                 override_analysis=False,
                                                 discarded=False
                                             ).exclude(
                                                 id__in=pop_list
                                             ).all()

        if spaces:
            for a, b in itertools.product(spaces, pspaces):
                try:
                    num = tlsh.diffxlen(a.fhash, b.fhash)
                    if num < 66: 
                        ''' If we find a match we add those spaces to our 
                            problem list'''
                        problem_spaces.append([model_to_dict(a,fields=fields),
                                               model_to_dict(b,fields=fields),
                                               num])
                        pop_list.append(b.id)
                except:
                    '''There are many ways this can make an exception for once
                    the spaces may not have a fhash because is missing data so
                    we take a look
                    '''
                    pass

            '''We filter the spaces yet again so the ones with a match problem 
            don't make the approved list'''
            pspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=False, discarded=False).exclude(id__in=pop_list).all()
            
            approved_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in pspaces])
        else:
            ''' If there are no spaces to compare we add all provision spaces
            to the approved list (yay?)'''
            approved_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in pspaces])

        # Lets add the discarded spaces
        dspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=False, discarded=True).all()
        discarded_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in dspaces])

        # Lets add the processed spaces
        pspaces = ProvisionalSpace.objects.filter(country=country, override_analysis=True, discarded=False).all()
        processed_spaces.extend([model_to_dict(pspace,fields=fields) for pspace in pspaces])
            
    data = request.GET.copy()
    if data and data.get("json_list"):
        return JsonResponse({'approved': approved_spaces,
                             'problem': problem_spaces,
                             'excluded': excluded_spaces,
                            })
    else:
        return render(request, 'space_analysis.html', {'approved': approved_spaces, 
                                                   'problem': problem_spaces,
                                                   'excluded': excluded_spaces,
                                                   'discarded': discarded_spaces,
                                                   'processed': processed_spaces
                                                   })

@staff_member_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_csv(request,request.FILES['file'])
            return HttpResponseRedirect('/analyze/provisional_spaces/')
    else:
        form = UploadFileForm()
    return render(request, 'space_upload.html', {'form': form})

def handle_csv(request,file):

        data_filename = file

        reverse_country_list = {name:code for code, name in countries}
        
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
                messages.error(request, 'The file has an error, to fix it you can open in libre office and save "Use Text CSV Format', extra_tags='alert')
                complete_spaces = []
            processed_spaces = []
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
                    # Added the many to many relationship
                    if ownership_obj:
                        new_space.ownership_type.add(ownership_obj)
                    if affiliation_obj:
                        new_space.network_affiliation.add(affiliation_obj)
                    if governance_obj:
                        new_space.governance_type.add(governance_obj)
                    new_space.save() 
                    
                except Exception as e:
                    #print (space.__dict__)
                    raise e
                    
def calculate_fhash(new_space):
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
    return tlsh.forcehash(space_string)

@staff_member_required
def provisional_space(request):
    fields = ['latitude','longitude','name','city','country','website', 'postal_code','email', 'province', 'address1', 'id']
    if request.method == 'GET':
        print(request)
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
        space = ProvisionalSpace.objects.filter(id=id[0]).first()
        if space:
            for key, value in data.items():
                setattr(space,key,value)
            space.fhash = calculate_fhash(space)
            space.save()
        return JsonResponse({'success':1})
    if request.method == "PUT":
        if(isinstance(request.body,(bytes, bytearray))):
            str_response = request.body.decode('utf-8')
            data = json.loads(str_response)
        else:
            data = json.loads(request.body)
        if data and data['id']:
            spaces_list = []
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
        spaces = ProvisionalSpace.objects.filter(discarded=True).delete()
        return JsonResponse({'success':1}, safe=False)
    if request.method == "PATCH":
        spaces = ProvisionalSpace.objects.filter(override_analysis=True).all()
        for space in spaces:
            new_space = Space()
            for field in space._meta.fields:
                if field.name not in ["id", "discarded", "override_analysis"]:
                    setattr(new_space, field.name, getattr(space, field.name))
            new_space.save()
            space.delete()
        return JsonResponse({'success':1}, safe=False)

@staff_member_required
def space_csv(request):

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
        space = Space.objects.filter(id=id[0]).first()
        if space:
            for key, value in data.items():
                setattr(space,key,value)
            space.fhash = calculate_fhash(space) 
            space.save()
        return JsonResponse({'success':1})
        