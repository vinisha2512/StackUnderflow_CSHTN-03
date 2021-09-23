from django.shortcuts import render
from django.core.mail import EmailMessage
# Create your views here.
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



def VerifyPageData():
    name=[]
    orderid=[]
    phone=[]
    plink=[]
    try:
        unveri=database.child("AdminV").child("UnVeri").get()
        for dets in unveri.each():
            OrderId=dets.key()
            print("order:",OrderId)
            body=dets.val()
            UID = body.get("UID")
            print(UID)
            link = body.get("PrescriptionLink")
            Userdets=database.child("Users").child(UID).child("Orders").child(OrderId).get()
            print(Userdets)
            Name = Userdets.val().get("Name")
            Phone = Userdets.val().get("Phone")
            name.append(Name)
            orderid.append(OrderId)
            phone.append(Phone)
            plink.append(link)
            print(name,orderid,phone,plink)
            combilis=zip(name,orderid,phone,plink)


        # History data fetch
        

    except:
        combilis=[]
    
    try:
        name1=[]
        orderid1=[]
        phone1=[]
        plink1=[]
        veri=database.child("AdminV").child("PrescVerified").get()
        for dets in veri.each():
            OrderId=dets.key()
            print("order:",OrderId)
            body=dets.val()
            UID = body.get("UID")
            link = body.get("PrescriptionLink")
            Name = body.get("Name")
            print(Name)
            Phone = body.get("Phone")
            name1.append(Name)
            orderid1.append(OrderId)
            phone1.append(Phone)
            plink1.append(link)
            print(name,orderid,phone,plink)
            combilis1=zip(name1,orderid1,phone1,plink1)
    except:
        combilis1=[]
        
    
        
    
    return [combilis,combilis1]





def prescriptionVerif(request):
    combilis= VerifyPageData()
    combilis1=combilis[0]
    combilis2=combilis[1]
    return render(request, "AdminVeri.html",{"data1": combilis1,"data2":combilis2})

def verify(request):
    oid=request.POST.get("order_id")
    pno=request.POST.get("phone")
    pli=request.POST.get("plink")
    nam=request.POST.get("name")

    foruid = database.child("AdminV").child("UnVeri").child(oid).get()
    UID = foruid.val().get("UID")

    Ud=database.child("Users").child(UID).child("Orders").child(oid).get()
    email1 = Ud.val().get("Email")
    d={
        "Name":nam,
        "Phone":pno,
        "UID":"UID",
        "PresciptionLink":pli,
    }
    database.child("AdminV").child("PrescVerified").child(oid).set(d)
    database.child("AdminV").child("UnVeri").child(oid).remove()
    scan={
        "Scan":1
    }
    try:
        database.child("Users").child(UID).child("Orders").child(oid).update(scan)
    except:
        pass
    try:
        html_content = "Genjh marao " 
        email = EmailMessage("Arey Mori Maiiyan", html_content,
                            "eat.project.314@gmail.com",[email1,] )
        email.content_subtype = "html"
        # email.attach_file('C:/pro/mysite/invoice.pdf')
        res = email.send()
    except Exception as e:
        print(e)


    combilis=VerifyPageData()
    combilis1=combilis[0]
    combilis2=combilis[1]
    
    return render(request, "AdminVeri.html",{"data1": combilis1,"data2":combilis2})


def reject(request):
    return render(request, "AdminVeri.html")
