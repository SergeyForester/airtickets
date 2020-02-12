from django.db import models

# Create your models here.
class SearchHistory(models.Model):
    user = models.CharField(max_length=150)
    departure = models.CharField(max_length=3)
    arrival = models.CharField(max_length=3)
    date = models.DateField()

class UserLocation(models.Model):
    ip = models.CharField(max_length=50)
    country = models.CharField(max_length=70)
    city = models.CharField(max_length=70)