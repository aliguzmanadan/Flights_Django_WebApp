from django.test import Client, TestCase
from django.db.models import Max


from .models import Airport, Flight, Passenger

# Create your tests here. We do this by extending the TestCase class
class FlightTestCase(TestCase):

    #We first create an initial setup, i.e. dummy data to run our tests on.
    def setUp(self):
        
        #Create airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        #Create flights
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    #We now create our tests as methds of this class

    def test_departures_count(self):
        """Check the amount of departures from an airport"""
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        """Check the amount of arrivals to an airport"""
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        """Check if a flight is valid"""
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        """Check if a flight is invalid because of destination"""
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        """Check if a flight is invalid because of duration"""
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    #Among the tests we can perform client tests, by creating a client object in Django and making requests using that object
    def test_index(self):
        """Tests the index function"""

        #Set up client to make requests
        c = Client()

        #Send get request to index page and store response
        response = c.get("/flights/")

        #make sure status code is 200, i.e. OK
        self.assertEqual(response.status_code, 200)

        #Make sure 3 flights are returned in the context. The context is the dictionary one passes to the template (see index in views.py)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c= Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        #Get max id of all flights available
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        #request an invalid flight page
        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        """Check if the passenger list per flight is generaed as expected"""
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c=Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        """Check if the non-passenger list per flight is generaed as expected"""
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)

#run "python manage.py test" in terminal to run these tests