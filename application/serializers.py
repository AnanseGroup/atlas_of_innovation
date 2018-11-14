from application.models.spaces import Space
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

class SpaceSerializer(CountryFieldMixin, serializers.ModelSerializer):
    validated = serializers.ReadOnlyField()
    recently_updated = serializers.ReadOnlyField()
    
    def __init__(self, *args, fields=None, **kwargs):

        super(SpaceSerializer, self).__init__(*args, **kwargs)
        # Drop any fields that are not specified in the `fields` argument.
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            existing.add('validated')
            existing.add('recently_updated')
            for field_name in existing - allowed:
                self.fields.pop(field_name)


    class Meta:
        model = Space
        # fields = (f.name for f in Space._meta.get_fields())
        fields = "__all__"