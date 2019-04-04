from django.db import models
from django.contrib.postgres.fields import JSONField
from django.forms import ModelForm
from django.urls import reverse
from captcha.fields import ReCaptchaField
from django_countries.fields import CountryField
from django import forms
from datetime import datetime, timedelta
from django.db.models.signals import post_save
#from application.views.mails import mails
from post_office.models import EmailTemplate
from post_office import mail
from .space_multiselectfields import GovernanceOption, OwnershipOption, AffiliationOption
from application.models.user import Moderator
from django.conf import settings
from django.contrib.auth.models import User
class Space(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)

    # In the form, we want to auto-fill lat/long from address or map using
    # google: https://developers.google.com/maps/documentation/geocoding/start
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # address fields inspired by https://help.wufoo.com/articles/en_US/kb/Address
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    country = CountryField(max_length=20, null=True, blank=True)
    additional_directions = models.CharField(max_length=255, null=True, blank=True)
    # public_trans = EnumField(PublicTransAccess, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)

    website = models.CharField(max_length=255, null=True, blank=True)
    date_opened = models.DateField(null=True, blank=True)
    date_closed = models.DateField(null=True, blank=True)
    short_description = models.CharField(max_length=140, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    last_updated = models.DateTimeField(null=False, auto_now=True)
    data_credit = models.CharField(max_length=100, null=True, blank=True)
    
    # It's the hash field for fuzzy comparing with tlsh
    fhash = models.CharField(max_length=500, null=True, blank=True)

    residencies = models.NullBooleanField(null=True, blank=True)
    membership = models.IntegerField(null=True, blank=True)
    users = models.IntegerField(null=True, blank=True)
    size_in_sq_meters = models.IntegerField(null=True, blank=True)
    wheelchair_accessibility = models.NullBooleanField(null=True, blank=True)
    business_model = models.CharField(max_length=1000, null=True, blank=True)
    hours_of_operation = models.CharField(max_length=1000, null=True, blank=True)

    IN_OPERATION = 'In Operation'
    PLANNED = 'Planned'
    CLOSED = 'Closed'
    STATUS_OPTIONS = (
        (IN_OPERATION, 'In Operation'),
        (PLANNED, 'Planned'),
        (CLOSED, 'Closed'),
    )
    operational_status = models.CharField(  
        max_length=12,
        choices=STATUS_OPTIONS,
        null=True, blank=True,
    )

    VERIFIED = 'Verified'
    FLAGGED = 'Flagged'
    VALIDATION_OPTIONS = (
        (VERIFIED, 'Verified Address and Operation Status'),
        (FLAGGED, 'Flagged'),
    )
    validation_status = models.CharField(
        max_length=8,
        choices=VALIDATION_OPTIONS,
        null=True, blank=True,
    )

    ownership_type = models.ManyToManyField(OwnershipOption, blank=True)
    governance_type = models.ManyToManyField(GovernanceOption, blank=True)
    network_affiliation = models.ManyToManyField(AffiliationOption, blank=True)

    other_data = JSONField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('space_profile', kwargs={'id':self.id})

    @property
    def validated(self):
        if self.validation_status == 'Verified':
            return True
        else:
            return False

    @property
    def recently_updated(self):
        d = datetime.utcnow() - timedelta(days=180)
        l = self.last_updated.replace(tzinfo=None)
        if ((l - d).days > 0):
            return False
        else:
            return False
    
def keep_track_save(sender, instance, created, **kwargs):
        if created:
          print("save")
post_save.connect(keep_track_save, sender=Space)
class ProvisionalSpace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)

    # In the form, we want to auto-fill lat/long from address or map using
    # google: https://developers.google.com/maps/documentation/geocoding/start
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # address fields inspired by https://help.wufoo.com/articles/en_US/kb/Address
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    country = CountryField(max_length=20, null=True, blank=True)
    additional_directions = models.CharField(max_length=255, null=True, blank=True)
    # public_trans = EnumField(PublicTransAccess, null=True, blank=True)
    
    # It's the hash field for fuzzy comparing with tlsh
    fhash = models.CharField(max_length=500, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)

    website = models.CharField(max_length=255, null=True, blank=True)
    date_opened = models.DateField(null=True, blank=True)
    date_closed = models.DateField(null=True, blank=True)
    short_description = models.CharField(max_length=140, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    last_updated = models.DateTimeField(null=False, auto_now=True)
    data_credit = models.CharField(max_length=100, null=True, blank=True)

    residencies = models.NullBooleanField(null=True, blank=True)
    membership = models.IntegerField(null=True, blank=True)
    users = models.IntegerField(null=True, blank=True)
    size_in_sq_meters = models.IntegerField(null=True, blank=True)
    wheelchair_accessibility = models.NullBooleanField(null=True, blank=True)
    business_model = models.CharField(max_length=1000, null=True, blank=True)
    hours_of_operation = models.CharField(max_length=1000, null=True, blank=True)
    
    ''' Stuff related to the analysis
        override_analysis skips the analysis and send this space directly
                          to the new space queue
        discarded skips the analysis and sends this space to the discarded
                  queue
    '''
    override_analysis = models.NullBooleanField(null=True, blank=True)
    discarded = models.NullBooleanField(null=True, blank=True)

    IN_OPERATION = 'In Operation'
    PLANNED = 'Planned'
    CLOSED = 'Closed'
    STATUS_OPTIONS = (
        (IN_OPERATION, 'In Operation'),
        (PLANNED, 'Planned'),
        (CLOSED, 'Closed'),
    )
    operational_status = models.CharField(  
        max_length=12,
        choices=STATUS_OPTIONS,
        null=True, blank=True,
    )

    VERIFIED = 'Verified'
    FLAGGED = 'Flagged'
    VALIDATION_OPTIONS = (
        (VERIFIED, 'Verified Address and Operation Status'),
        (FLAGGED, 'Flagged'),
    )
    validation_status = models.CharField(
        max_length=8,
        choices=VALIDATION_OPTIONS,
        null=True, blank=True,
    )

    ownership_type = models.ManyToManyField(OwnershipOption, blank=True)
    governance_type = models.ManyToManyField(GovernanceOption, blank=True)
    network_affiliation = models.ManyToManyField(AffiliationOption, blank=True)

    other_data = JSONField(null=True, blank=True)
    
    class Meta:
        permissions = (
            ("analyse_provisional_spaces", "Grants permission to use the analyser"),
            ("upload_provisonal_spaces", "Grants permission to use the uploader"),
        )

    def get_absolute_url(self):
        return reverse('space_profile', kwargs={'id':self.id})

    @property
    def validated(self):
        if self.validation_status == 'Verified':
            return True
        else:
            return False

    @property
    def recently_updated(self):
        d = datetime.utcnow() - timedelta(days=180)
        l = self.last_updated.replace(tzinfo=None)
        if ((l - d).days > 0):
            return False
        else:
            return False
 
class DataCreditLog(models.Model):
    '''Logs the edit credits made to the spaces
    '''
    id = models.AutoField(primary_key=True)
    space_id = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    credit = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=False, auto_now=True)
    is_provisional=models.BooleanField(default=False)#used for provisional spaces
class SpaceForm(ModelForm):

    captcha = ReCaptchaField()
    ownership_type =  forms.ModelMultipleChoiceField(
        queryset=OwnershipOption.objects.all(), to_field_name="description", required=False)
    governance_type =  forms.ModelMultipleChoiceField(
        queryset=GovernanceOption.objects.all(), to_field_name="description", required=False)
    network_affiliation =  forms.ModelMultipleChoiceField(
        queryset=AffiliationOption.objects.all(), to_field_name="description", required=False)

    def __init__(self, *args, **kwargs):
        super(SpaceForm, self).__init__(*args, **kwargs)
        self.fields.pop('email')
        self.fields.pop('phone')

    class Meta:
        model = Space
        fields = '__all__'
class Suggestion(models.Model):
    '''Model for sugested changes entry, it can have more than one Field suggestion'''
    id= models.AutoField(primary_key=True)
    space = models.ForeignKey(
        Space, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    active= models.BooleanField(default=True)
    date=models.DateTimeField(auto_now_add=True)
class FieldSuggestion(models.Model):
    '''Model that store the field suggestion'''
    id = models.AutoField(primary_key=True)
    suggestion = models.ForeignKey(
        Suggestion, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=500, null=True, blank=True)
    field_suggestion = models.CharField(max_length=500, null=True, blank=True)
class Owners(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    space= models.ForeignKey(Space, on_delete= models.CASCADE)
User._meta.get_field('email').__dict__['_unique'] = True