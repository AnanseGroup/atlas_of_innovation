from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from application.models import Space
import csv

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('data_file_csv', type=str)

    def handle(self, *args, **options):
        data_filename = options['data_file_csv']
        with open(data_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            # replace empty strings with None
            complete_spaces = [{key: value if not value == '' else None for key, value in row.items()} for row in reader]
            processed_spaces = []
            for space in complete_spaces:
                processed_space = {}
                for field in Space._meta.get_fields():
                    processed_space[field.name]=space.pop(field.name, None)
                processed_space['other_data'] = space
                processed_spaces.append(processed_space)
            spaces = [Space(**space) for space in processed_spaces]
            for space in spaces:
                try:
                    space.clean_fields()
                except ValidationError as v:
                    for field in v.error_dict:
                        space.other_data[field] = space.__dict__[field]
                        setattr(space, field, None)
                try:
                    space.save()
                except Exception as e:
                    print (space.__dict__)
                    raise e
