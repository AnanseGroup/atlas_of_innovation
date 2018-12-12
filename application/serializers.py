from application.models.spaces import Space
from rest_framework import serializers
from urllib.parse import urlparse, ParseResult
from django_countries.serializers import CountryFieldMixin

class SpaceSerializer(CountryFieldMixin, serializers.ModelSerializer):

    def __init__(self, *args, fields=None, **kwargs):

        super(SpaceSerializer, self).__init__(*args, **kwargs)
        # Drop any fields that are not specified in the `fields` argument.
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        myfield_val = instance.website
        output = super(SpaceSerializer, self).to_representation(instance)
        if myfield_val:
            # Parse the url in case it doesn't have http
            p = urlparse(myfield_val, 'http')
            netloc = p.netloc or p.path
            path = p.path if p.netloc else ''
            p = ParseResult('http', netloc, path, *p[3:])
            output['website'] = p.geturl()
        else:
            output['website'] = myfield_val
        return output
        
    class Meta:
        model = Space
        # fields = (f.name for f in Space._meta.get_fields())
        fields = "__all__"