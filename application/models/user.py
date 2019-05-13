from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(max_length=20, null=True, blank=True)