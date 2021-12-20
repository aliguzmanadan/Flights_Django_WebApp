from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey

import flights

# Create your models here.

#Airport class
class Airport(models.Model):
    code = CharField(max_length=3)
    city = CharField(max_length=64)

    def __str__(self):
        return  f"{self.city} ({self.code})"


#Flight class that takes info from Airport
class Flight(models.Model):
    origin = ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}" 

    #Method to verify that a flight is a valid flight
    def is_valid_flight(self):
        return self.origin != self.destination and self.duration > 0

#Passenger class
class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"