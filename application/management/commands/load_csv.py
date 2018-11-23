from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from application.models import Space, DataCreditLog
from application.models.space_multiselectfields import GovernanceOption, OwnershipOption, AffiliationOption
from django_countries import countries
import csv
import datetime

class Command(BaseCommand):
    help = 'Loads a CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('data_file_csv', type=str)

    def handle(self, *args, **options):
        data_filename = options['data_file_csv']

        reverse_country_list = {name:code for code, name in countries}

        with open(data_filename, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            # replace empty strings with None
            complete_spaces = [{key: value if not value == '' else None \
                                for key, value in row.items()} for row in reader]
            processed_spaces = []
            for space in complete_spaces:
                processed_space = {}

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
                for field in Space._meta.get_fields():
                    if not field.name in processed_space:
                        # (PEDRO) To solve #85 remove the many to many fields
                        if type(field).__name__ is not "ManyToManyField":
                            processed_space[field.name]=space.pop(field.name, None)
                space = {field:space[field] for field in space if space[field]}
                processed_space['other_data'] = space
                #processed_spaces.append(processed_space)
                
                '''(Pedro) Removed the for loop, there may be a performance hit
                    but I did it to add the ManyToMany relationships'''
                new_space = Space(**processed_space)
                try:
                    new_space.clean_fields()
                except ValidationError as v:
                    for field in v.error_dict:
                        new_space.other_data[field] = new_space.__dict__[field]
                        setattr(new_space, field, None)
                try:
                    new_space.save()
                    # Added the many to many relationship
                    if ownership_obj:
                        new_space.ownership_type.add(ownership_obj)
                    if affiliation_obj:
                        new_space.network_affiliation.add(affiliation_obj)
                    if governance_obj:
                        new_space.governance_type.add(governance_obj)
                    new_space.save()
                    data_credit = {
                               'ip_address': '127.0.0.1',
                               'space_id': new_space.id,
                               'credit': 'CSV / '+new_space.data_credit
                              }
                    new_data_credit = DataCreditLog(**data_credit)
                    new_data_credit.save()
                    
                except Exception as e:
                    print (space.__dict__)
                    raise e
