from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from application.models import Space, DataCreditLog
from application.models.space_multiselectfields import GovernanceOption, OwnershipOption, AffiliationOption
from django_countries import countries
import tlsh
import datetime

class Command(BaseCommand):
    help = 'Creates the fuzzy hash for the spaces stored in the database' 

    def handle(self, *args, **options):
        i = 0

        # To convert None to an empty string
        xstr = lambda s: '' if s is None else str(s)

        spaces = Space.objects.all()
        #spaces = spaces.filter(country__in=["US"])
        for space in spaces:
            space_info = [space.name]
            if space.address1:
                space_info.append(space.address1)
            if space.city:
                space_info.append(space.city)
            if space.province:
                space_info.append(space.province)
            if space.country:
                space_info.append(str(space.country))
            if space.postal_code:
                space_info.append(space.postal_code)
            space_stuff = " ".join(space_info).replace(",", "").replace("-","").replace(".","").replace("_","").replace("+","")
            space_string = ' '.join(space_stuff.split()).encode("utf-8")
            print(space.id)
            print(str(space_string) + ":" + str(len(space_string)))
            space.fhash = tlsh.forcehash(space_string)
            print(space.fhash)
            print("-----------------------------------------------------------")
            space.save()