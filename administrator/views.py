from django.template.loader import render_to_string
from django.template.loader import get_template
from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
# Create your views here.
from django.shortcuts import render
import os
import pyrebase
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from .utils import render_to_pdf

load_dotenv('\.env')
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
    name = []
    orderid = []
    phone = []
    plink = []
    try:
        unveri = database.child("AdminV").child("UnVeri").get()
        for dets in unveri.each():
            OrderId = dets.key()
            print("order:", OrderId)
            body = dets.val()
            UID = body.get("UID")
            print(UID)
            link = body.get("PrescriptionLink")
            Userdets = database.child("Users").child(
                UID).child("Orders").child(OrderId).child("Details").get()
            print(Userdets)
            Name = Userdets.val().get("Name")
            Phone = Userdets.val().get("Phone")
            name.append(Name)
            orderid.append(OrderId)
            phone.append(Phone)
            plink.append(link)
            print(name, orderid, phone, plink)
            combilis = zip(name, orderid, phone, plink)

        # History data fetch

    except:
        combilis = []

    try:
        name1 = []
        orderid1 = []
        phone1 = []
        plink1 = []
        veri = database.child("AdminV").child("PrescVerified").get()
        for dets in veri.each():
            OrderId = dets.key()
            print("order:", OrderId)
            body = dets.val()
            UID = body.get("UID")
            link = body.get("PrescriptionLink")
            Name = body.get("Name")
            print(Name)
            Phone = body.get("Phone")
            name1.append(Name)
            orderid1.append(OrderId)
            phone1.append(Phone)
            plink1.append(link)
            print(name, orderid, phone, plink)
            combilis1 = zip(name1, orderid1, phone1, plink1)
    except:
        combilis1 = []

    return [combilis, combilis1]


def prescriptionVerif(request):
    combilis = VerifyPageData()
    combilis1 = combilis[0]
    combilis2 = combilis[1]
    return render(request, "AdminVeri.html", {"data1": combilis1, "data2": combilis2})


def verify(request):
    oid = request.POST.get("order_id")
    pno = request.POST.get("phone")
    pli = request.POST.get("plink")
    nam = request.POST.get("name")

    foruid = database.child("AdminV").child("UnVeri").child(oid).get()
    UID = foruid.val().get("UID")

    Ud = database.child("Users").child(UID).child("Orders").child(oid).child("Details").get()
    email1 = Ud.val().get("Email")
    d = {
        "Name": nam,
        "Phone": pno,
        "UID": "UID",
        "PresciptionLink": pli,
    }
    database.child("AdminV").child("PrescVerified").child(oid).set(d)
    database.child("AdminV").child("UnVeri").child(oid).remove()
    scan = {
        "Scan": 1
    }
    try:
        database.child("Users").child(UID).child(
            "Orders").child(oid).child("Details").update(scan)
    except:
        pass
    try:
        # html_content = loader.get_template("templates/AdminVeri.html").render()
        # email = EmailMessage("Arey Mori Maiiyan", html_content,
        #                     "eat.project.314@gmail.com",[email1,] )
        # email.content_subtype = "html"
        # # email.attach_file('C:/pro/mysite/invoice.pdf')
        # res = email.send()
        ctx = {
        'shipment_id': "www.google.com"
        }
        html_body = render_to_string("mail.html",ctx)
        msg = EmailMultiAlternatives(subject="Verified!", from_email="eat.project.314@gmail.com",
                                     to=[email1, ], body=html_body)
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        dict1 = {"data": "x", "data2": ["1", "2", "3"], "data3": 5}
        pdf = render_to_pdf('invoice.html', dict1)
    except Exception as e:
        print("abcd", e)

    combilis = VerifyPageData()
    combilis1 = combilis[0]
    combilis2 = combilis[1]

    return render(request, "AdminVeri.html", {"data1": combilis1, "data2": combilis2})


def reject(request):
    oid = request.POST.get("order_id1")
    pno = request.POST.get("phone1")
    pli = request.POST.get("plink1")
    nam = request.POST.get("name1")
    foruid = database.child("AdminV").child("UnVeri").child(oid).get()
    UID = foruid.val().get("UID")
    Ud = database.child("Users").child(UID).child("Orders").child(oid).child("Details").get()
    database.child("AdminV").child("UnVeri").child(oid).remove()
    database.child("Users").child(UID).child("Orders").child(oid).remove()
    
    email1 = Ud.val().get("Email")
    try:
        html_content = "Your Order Request was rejected unfortunately due to some problems in your precription.<br>For any Queries please contact us using the following details<br>Number: 9167386883<br>Email-id:medistop@gmail.com"
        email = EmailMessage("Order request rejected!", html_content,
                             "eat.project.314@gmail.com", [email1, ])
        email.content_subtype = "html"
        res = email.send()
    except:
        pass

    combilis = VerifyPageData()
    combilis1 = combilis[0]
    combilis2 = combilis[1]

    return render(request, "AdminVeri.html", {"data1": combilis1, "data2": combilis2})


# Shipment

def ShipmentPageData():
    name = []
    orderid = []
    phone = []
    ilink = []
    try:
        veri = database.child("AdminV").child("Veri").get()
        for dets in veri.each():
            OrderId = dets.key()
            print("order:", OrderId)
            body = dets.val()
            UID = body.get("UID")
            print(UID)
            link = body.get("InvoiceLink")
            Userdets = database.child("Users").child(
                UID).child("Orders").child(OrderId).child("Details").get()
            print(Userdets)
            Name = Userdets.val().get("Name")
            Phone = Userdets.val().get("Phone")
            if (Userdets.val().get("Scan")==3):
                continue
            name.append(Name)
            orderid.append(OrderId)
            phone.append(Phone)
            ilink.append(link)
        print(name, orderid, phone, ilink)
        combilis = zip(name, orderid, phone, ilink)
        print(combilis)
        return combilis

        # History data fetch

    except:
        return []

    
    

def ShipmentVeri(request):
    combilis = ShipmentPageData()
    print(combilis)

    return render(request, "QRCode.html", {"data1": combilis})


def read_qr(request):
    if request.method=="POST":
        order_id = request.POST.get('order_id')
        try:
            x=database.child("AdminV").child("Veri").child(order_id).get()
            print(x)
            y=x.val().get("UID")
            il=x.val().get("InvoiceLink")
            print(y)
            z=dict(database.child("Users").child(y).child("Orders").child(order_id).child("content").get().val())
            z1=dict(database.child("Users").child(y).child("Orders").child(order_id).child("Details").get().val())
            print(z)
            s=z1.get("Scan")
            d=z1.get("Date")
            print(s)
            
            if s>=3:
                s=3
                inlink={"Url":il}

                database.child("Users").child(y).child("PastOrders").child(d).child("Medicines").set(z)
                database.child("Users").child(y).child("PastOrders").child(d).child("Invoice").set(inlink)


                database.child("Users").child(y).child("Orders").child(order_id).remove()
            else:
                s=s+1
                scan = {"Scan": s}
                database.child("Users").child(y).child("Orders").child(order_id).child("Details").update(scan)
            print("correct")
            combilis = ShipmentPageData()
            
            return render(request, "QRCode.html", {"data1": combilis})

            #updation of scan var is left
        except Exception as e:
            print("not a valid qr code")
            print(e)
            return render(request, "QRCode.html")
    return render(request, "QRCode.html")





# inventory
def update(request):
    qty=request.POST.get('quantity')
    medname=request.POST.get('name')
    print(medname)

    database.child("Medicine").child(medname).update({"Quantity":qty})


    print("Hii")
    return HttpResponse('')


def dele(request):
    medname=request.POST.get('name')
    print(medname)

    database.child("Medicine").child(medname).update({"Quantity":0})


    print("Hi2i")
    return HttpResponse('')



def invent(request):
    
    count=0
    stock=[]
    names=[]
    manu=[]
    mrp=[]
    quan=[]
    index=[]

    stock2=[]
    names2=[]
    manu2=[]
    mrp2=[]
    quan2=[]
    
    meds_data=database.child("Medicine").get()
    for x in meds_data.each():
        # print(x.val()['Price'])
        index.append(count+1)
        names.append(x.key())
        manu.append(x.val()['Company'])
        mrp.append(x.val()['Price'])
        quan.append(x.val()['Quantity'])

        if(int(x.val()['Quantity'])<=3):
            names2.append(x.key())
            manu2.append(x.val()['Company'])
            mrp2.append(x.val()['Price'])
            quan2.append(x.val()['Quantity'])
        # val=[x.key(),x.val()['Company'],x.val()['Price'],x.val()['Quantity']]
        count=count+1
        
        if count==20:
            break
    stock=zip(index,names,manu,mrp,quan)
    stock2=zip(index,names2,manu2,mrp2,quan2)

    #print(stock)
    print("hello")


    return render(request,'inventory.html',{"data":stock,"data2":stock2})

    #admin-dashboard

def admindash(request):

   return render(request,'adminDashboard (1).html') 