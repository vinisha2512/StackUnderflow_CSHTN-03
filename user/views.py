from django.shortcuts import render
import os
import pyrebase
# Create your views here.

config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId": os.getenv("appId"),
    "measurementId": os.getenv("measurementId"),
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def xyz(request):
    return render(request, "home.html")

def retprod(request):
    meds = list(database.child("Medicine").shallow().get().val())
    data = {"meds":"_".join(meds)}
    return render(request, "index.html", data)
