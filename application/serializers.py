from application.models.spaces import Space
from rest_framework import serializers

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        # fields = (f.name for f in Space._meta.get_fields())
        fields = "__all__"