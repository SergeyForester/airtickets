import json
from datetime import datetime

from django.db import models


# Create your models here.

class Aircompany(models.Model):
    name = models.CharField(max_length=200, unique=True)
    rating = models.IntegerField()


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3)
    location = models.CharField(max_length=100)


class Flight(models.Model):
    departure_point = models.ForeignKey(Airport, default='default_from', on_delete=models.CASCADE,
                                        related_name='Airport.name+')
    to = models.ForeignKey(Airport,default='default_to', on_delete=models.CASCADE, related_name='Airport.name+')
    aircompany = models.ForeignKey(Aircompany, on_delete=models.CASCADE)


class Depature(models.Model):
    name = models.CharField(max_length=30)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, default=None)
    plane = models.CharField(max_length=50)
    depature_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    number_of_seats = models.PositiveIntegerField()

    def get_depature_info(self):
        return {'name': self.name, 'plane': self.plane, 'depature': self.depature_time, 'arrival': self.arrival_time}



class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    passport_data = models.CharField(max_length=1000)  # это словарь, преабразовывающийся с помощью json.loads()
    date_of_birth = models.DateField()

    def person_birth_date(self):
        return self.date_of_birth

    def person_full_name(self):
        return f'{self.name} {self.surname}'


class SeatType(models.Model):
    aircompany = models.ForeignKey(Aircompany, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    features = models.CharField(max_length=500)  # Это список


class Seat(models.Model):
    code = models.CharField(max_length=3)
    type = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=Person)
    price = models.PositiveIntegerField()
    is_busy = models.BooleanField(default=False)
    depature = models.ForeignKey(Depature, on_delete=models.CASCADE, default='')

    def book_seat(self, client):
        self.person = client
        self.is_busy = True
