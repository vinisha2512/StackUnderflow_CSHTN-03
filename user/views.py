from django.shortcuts import render
import os
import pyrebase
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv('\.env')
from django.http.response import HttpResponse

# Create your views here.
# print(os.getenv("apiKey"))
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


def homepage(request):
    return render(request, "trial.html")


def login(request):
    print("x")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            uid=user['localId']
            request.session['uid']=uid
            

        except:
            message = "Invalid ID or Password"
            print("Error email")
            return render(request, "login.html")
        
        # print(userinfo)
        return redirect("homepage.html")
    return render(request, "login.html")



def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phonenumber = request.POST.get("phonenumber")
        name = request.POST.get("name")
        password = request.POST.get("password")

        try:
            user = authe.create_user_with_email_and_password(email, password)
            uid = user['localId'] 

            data = {
                "Name":name,
                "Email":email,
                "Phone":phonenumber,
                "Address":"-"
            }
            request.session['uid']=uid
            database.child("Users").child(uid).child("Details").child("1").set(data)


            return render(request,"homepage.html")       
        except:
            message = "Unsuccessful in signing up, try again"
            print("Error email")
            return render(request, "login.html")
        
        # uid = user['localId']
    
       

        # print(userinfo)
        return redirect("dashboard")
    return render(request, "signup.html")


def reset(request):
    email = request.POST.get("email")
    authe.send_password_reset_email(email)
    return render(request, "login.html")

