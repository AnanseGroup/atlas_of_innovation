from django.db import models
from django.contrib.postgres.fields import JSONField
from django.forms import ModelForm
from django.urls import reverse
from captcha.fields import ReCaptchaField
from django import forms


class Space(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)

    # In the form, we want to auto-fill lat/long from address or map using
    # google: https://developers.google.com/maps/documentation/geocoding/start
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    # There is some stuff we have to do with Django REST Framework,
    # https://github.com/SmileyChris/django-countries/ The last point in the
    # documentation (https://github.com/SmileyChris/django-countries/) says
    # how to return the full country name.  This would be nice to do, because
    # it will make it easier to consume for unsophisticated consumers.
    country = models.CharField(max_length=20, null=True, blank=True)
    additional_directions = models.CharField(max_length=255, null=True, blank=True)
    # public_trans = EnumField(PublicTransAccess, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    # internationalize with https://github.com/stefanfoulis/django-
    # phonenumber-field/tree/master/phonenumber_field
    phone = models.CharField(max_length=15, null=True, blank=True)

    website = models.CharField(max_length=255, null=True, blank=True)
    date_founded = models.DateField(null=True, blank=True)
    short_description = models.CharField(max_length=140, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    residencies = models.NullBooleanField(null=True, blank=True)
    last_updated = models.DateTimeField(null=False, auto_now=True)
    data_credit = models.CharField(max_length=100, null=True, blank=True)

    other_data = JSONField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('space_profile', kwargs={'id':self.id})

class SpaceForm(ModelForm):
    
    captcha = ReCaptchaField()

    class Meta:
        model = Space
        fields = '__all__'