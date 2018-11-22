from django.db import models

class OwnershipOption(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=75)

    def __str__(self):
        return self.description

class GovernanceOption(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=75)

    def __str__(self):
        return self.description

class AffiliationOption(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=75)

    def __str__(self):
        return self.description