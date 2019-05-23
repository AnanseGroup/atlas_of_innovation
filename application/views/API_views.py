# These views render the database as JSON
from django.shortcuts import render
from django.core import serializers
from application.serializers import SpaceSerializer
from application.models import Space
from django.http import HttpResponse,JsonResponse
from django.db.models import Q

def filter_spaces(request):
    '''**These views render the database as JSON**'''
    filter_terms = request.GET
    spaces = Space.objects.all()
    allfields=1

    if 'name' in filter_terms:
        spaces = spaces.filter(name__icontains=filter_terms['name'])

    if 'all_text' in filter_terms:
        spaces = spaces.filter(Q(name__icontains=filter_terms['all_text']) |
                               Q(description__icontains=filter_terms['all_text']) |
                               Q(short_description__icontains=filter_terms['all_text']))

    if 'country' in filter_terms:
        countries = filter_terms['country'].split(",")
        spaces = spaces.filter(country__in=countries)

    if 'operational_status' in filter_terms:
        if filter_terms['operational_status'] == "null":
            spaces = spaces.filter(operational_status__isnull=True)
        else:
            spaces = spaces.filter(operational_status__iexact=\
                                filter_terms['operational_status'])

    if 'not_closed' in filter_terms:
        spaces = spaces.exclude(operational_status__iexact="Closed")

    if 'network_affiliation' in filter_terms:
        spaces = spaces.filter(network_affiliation__name=filter_terms['network_affiliation'])

    fields = ['latitude','longitude','name','city','country','website','short_description','id']
    if 'fields' in filter_terms:
         fields = set(fields) & set(filter_terms['fields'].split(","))
    fields2 = list(fields)
    if spaces is not None and not 'not_extend' in filter_terms:
       fields2.extend(['validated', 'recently_updated'])
    print(spaces)
    serializer = SpaceSerializer(spaces, fields=fields2, many=True)

    return JsonResponse(serializer.data, safe=False)

# We're not going to allow for programmatic creation/editing/deleting for fear
# that there will be spambots that take advantage of those features and ruin
# the database
