from django.shortcuts import render

# Create your views here.


def home(req):
    return render(req, "home.html")


def login(req):
    return render(req, "login.html")
