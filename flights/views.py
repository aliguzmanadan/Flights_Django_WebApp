from django.http import request, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse


from .models import Flight, Passenger

import flights

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk = flight_id)     #pk is primary key in Django
    except Flight.DoesNotExist:
        raise Http404("Fligth does not exist")
        
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    
    #For a post request, add a new flight
    if request.method == "POST":

        #Access the flight
        flight = Flight.objects.get(pk=flight_id)

        #Finding passenger id submitted from the form
        passenger_id = int(request.POST["passenger"])

        #Finding the passenger based on the id
        passenger = Passenger.objects.get(pk = passenger_id)

        #Adding passenger to the flight
        passenger.flights.add(flight)

        #redirect user to the flight page
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
