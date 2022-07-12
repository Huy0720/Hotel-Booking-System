from django.db import models

# Create your models here.
#class SearchCountry(models.Model):
    #countryname = models.CharField(max_length=250)

class SearchDestination(models.Model):
    country = models.CharField(max_length=250)
    people = models.PositiveIntegerField()
    #rooms = models.PositiveIntegerField()
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    