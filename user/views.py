from django.shortcuts import render
import os
import pyrebase
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv('\.env')
from django.http.response import HttpResponse, HttpResponseRedirect

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


def myuser_login_required(f):
    def wrap(request, *args, **kwargs):
        if 'member_id' not in request.session.keys():
            return HttpResponseRedirect("/login")
        return f(request, *args, **kwargs)
    wrap._doc_ = f._doc_
    wrap._name_ = f._name_
    return wrap

def xyz(request):
    return render(request, "home.html")

def retprod(request):
    meds = list(database.child("Medicine").shallow().get().val())
    data = {"meds":"_".join(meds)}
    return render(request, "index.html", data)


def homepage(request):
    meds = list(database.child("Medicine").shallow().get().val())
    data = {"meds":"_".join(meds)}
    return render(request, "Home.html", data)

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        try:
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            uid=user['localId']
            request.session['uid']=uid
            request.session['loggedin'] = True
        except:
            message = "Invalid ID or Password"
            print("Error email")
            return render(request, "Home.html") #error message dikhana padega
        return redirect(homepage)
    return render(request, "Home.html")



def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phonenumber = request.POST.get("phonenumber")
        print(" ", phonenumber)
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
            request.session['loggedin'] = True
            database.child("Users").child(uid).child("Details").child("1").set(data)
            return render(request,"Home.html")       
        except:
            message = "Unsuccessful in signing up, try again"
            print("Error email")
            return render(request, "Home.html")  #error message dikhana padega
        # uid = user['localId']
        # print(userinfo)
        return redirect("dashboard")
    return render(request, "signup.html")


def reset(request):
    email = request.POST.get("email")
    authe.send_password_reset_email(email)
    return render(request, "Home.html")

def med_class(request,category):
    # fetching info for a therapeutic class
    import pandas as pd
    data1=[]
    classa = category
    col_list = ["Medicine_Name","Type_of_Sell","MRP","Therapeutic_Class","Url"]

    df=pd.read_csv('New_Sample.csv',usecols=col_list)
    newdf=df.query('Therapeutic_Class == "{0}"'.format(classa))
    sending=newdf.values.tolist()
    return render(request,"SeeAll.html",{"data1":sending[:5], "data2":sending[5:10], "data3":sending[10:15], "data4":sending[15:20], "class":category})

def med_deets(request,MEDNAME):
    import pandas as pd
    data1=[]
    classa = MEDNAME
    df=pd.read_csv('New_Sample.csv')
    newdf=df.query('Medicine_Name == "{0}"'.format(classa))

    data_array=newdf.values.tolist()
    
    values=data_array[0]
    name=values[0]
    presc=values[1]
    if(presc=="N"):
        presc="No prescription required"
    typeofsell=values[2]
    manu=values[3]
    salt=values[4].split('+')


    mrp=values[5]
    uses=values[6].split(',')
    uses.pop()
    alter=values[7].split(',')
    alter.pop()
    side=values[8].split(',')
    side.pop()
    howto=values[9].split('.')
    howto.pop()
    chemical=values[10]
    habit=values[11]
    thera=values[12]
    action=values[13]
    url=values[14]
    med_name = name
    name = name.replace(".", ",")
    qty_left=int(dict(database.child("Medicine").child(name).get().val())["Quantity"])
    temp=int(dict(database.child("Medicine").child(name).get().val())["Temp"])
    qty_left=min(qty_left-temp,5)
    
    return render(request,"index__1.html",{"name":med_name,"pres":presc,"qty_left":qty_left,"typeofsell":typeofsell,"manu":manu,"salt":salt,"mrp":mrp,"uses":uses,"alter":alter,"side":side,"howto":howto,"chem":chemical,"habbit":habit,"thera":thera,"action":action,"url":url})

def addtocart(request):
    medname=request.POST.get('name')
    print(medname)
    number=int(request.POST.get('quantity'))
    UID= "Rsz5MPwnYhbpNV6D42qorchrvBH3"
    # quan_left = int(dict(database.child("Medicine").child(med_name).get().val())["Quantity"])
    noofmeets = int(dict(database.child("Medicine").child(medname).get().val())["Temp"]) + number
    try:
        value_in_cart = int(dict(database.child("Users").child(UID).child("Cart").child(medname).get().val())["Quantity"]) + number
        database.child("Users").child(UID).child("Cart").child(medname).set({"Quantity":value_in_cart})

    except:

        database.child("Users").child(UID).child("Cart").child(medname).set({"Quantity":number})
    database.child("Medicine").child(medname).update({"Temp": noofmeets})



    qty_left=int(dict(database.child("Medicine").child(medname).get().val())["Quantity"])
    temp=int(dict(database.child("Medicine").child(medname).get().val())["Temp"])
    qty_left=min(qty_left-temp,5)
    return HttpResponse(qty_left)
