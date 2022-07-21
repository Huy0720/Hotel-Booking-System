from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SearchDestination(models.Model):
    country = models.CharField(max_length=250)
    people = models.PositiveIntegerField()
    #rooms = models.PositiveIntegerField()
    checkin_date = models.DateField()
    checkout_date = models.DateField()

class Customer(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
