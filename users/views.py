from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    #If no user is signed in, return to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        #Accessing username and password from the data
        username = request.POST["username"]
        password = request.POST["password"]

        #Check if username and passwrod are correct, returning user object if so. Otherwise this resurns None
        user = authenticate(request, username=username, password=password)

        #If user is returned, loig in and go to index page
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))  #The needed info here is passed via the request.
        #Otherwise return to login page withdifferent content.
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out"
    })