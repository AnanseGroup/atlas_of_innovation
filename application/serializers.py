from application.models.spaces import Space
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

class SpaceSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Space
        # fields = (f.name for f in Space._meta.get_fields())
        fields = "__all__"