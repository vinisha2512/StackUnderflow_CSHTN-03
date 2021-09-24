from django.shortcuts import render
import os
import pyrebase
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv('\.env')
from django.http.response import HttpResponse
import pandas as pd
from django.core.files.storage import default_storage

from PIL import Image
import os, io
from google.cloud import vision_v1
import difflib
import csv
from google.cloud.vision_v1 import types
import pathlib
from pdf2image import convert_from_path
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# importing get_template from loader
from django.template.loader import get_template

# import render_to_pdf from util.py
from .utils import render_to_pdf

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

def f1(request):
    if request.method =='POST':
        # print(name,quan)
        hell="yes"
        UID= request.session['uid']
        med_name=request.POST.get('name')
        quantity=request.POST.get('quantity')
        print("Hola", UID, quantity)
        try:
            value_in_cart = int(dict(database.child("Users").child(UID).child("Cart").child(med_name).get().val())["Quantity"]) + quantity
            database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":value_in_cart})
        except:

            database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":quantity})
        # database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":quantity})
                                                                        # quantity lena chahiye yaa +1 ye doubt hai 
        quan_left = int(dict(database.child("Medicine").child(med_name).get().val())["Quantity"])
        noofmeets = int(dict(database.child("Medicine").child(med_name).get().val())["Temp"]) + 1
        # value_in_cart = int(dict(database.child("Users").child(UID).child("Cart").child(med_name).get().val())["Quantity"]) + 1
        
        if(quan_left-noofmeets<=0):
            hell="no"

        # database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":value_in_cart})
        database.child("Medicine").child(med_name).update({"Temp": noofmeets})

        return HttpResponse(hell)



def f2(request):
    if request.method =='POST':
        # print(name,quan)
        hell="yes"
        UID= "Rsz5MPwnYhbpNV6D42qorchrvBH3"
        med_name=request.POST.get('name')
        # quantity=request.POST.get('quantity')
        
        # database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":quantity})
                                                                        # quantity lena chahiye yaa +1 ye doubt hai 
        # quan_left = int(dict(database.child("Medicine").child(med_name).get().val())["Quantity"])
        noofmeets = int(dict(database.child("Medicine").child(med_name).get().val())["Temp"]) - 1
        value_in_cart = int(dict(database.child("Users").child(UID).child("Cart").child(med_name).get().val())["Quantity"]) - 1
        


        database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":value_in_cart})
        database.child("Medicine").child(med_name).update({"Temp": noofmeets})

        return HttpResponse("")
        # name=request.POST.get('name')
        # quan=request.POST.get('quantity')
        # print(name,quan)
        # hell = "yes"
        # return HttpResponse(hell)

def delete(request):
    if request.method =='POST':
        name=request.POST.get('name')
        uid=request.POST.get('uid')
        database.child("Users").child(uid).child("Cart").child(name).remove()
        # quan=request.POST.get('quantity')
        print(name)
        print("delete row: ",name)
        hell = "yes"
        return HttpResponse(hell)


def upload(request):
    return render(request, "upload-prescription.html")

def read_presc(request):
    if request.method == 'POST':
        file = request.FILES['file']
        imagename = file.name
        ext = pathlib.Path(imagename).suffix

        file_save = default_storage.save(imagename, file)
        ref = storage.child("Prescription").child(request.session["uid"]).put("media/" + imagename)
        

        def function():
            try:
                downloadurl = storage.child("Prescripton").child(request.session["uid"]).get_url(None)
                return downloadurl
            except:
                downloadurl= ""
                return downloadurl
        
        ext = pathlib.Path(imagename).suffix

        # if ext==".pdf":
        #     images = convert_from_path('example.pdf')
        #     for i in range(len(images)):
        #         images[i].save('page'+ str(i) +'.jpg', 'JPEG')

        # #Reading prescription photo for dr and date tag
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ascendant-choir-326117-f6d97fe48d5c.json' #path
        client = vision_v1.ImageAnnotatorClient()

        FOLDER_PATH = r'media/' #prescription path
        # # IMAGE_FILE = './fromfrontend/'+imagename
        IMAGE_FILE = imagename
        FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

        with io.open(FILE_PATH, 'rb') as image_file:
            content = image_file.read()


        image = vision_v1.types.Image(content=content)
        response = client.document_text_detection(image=image)

        docText = response.full_text_annotation.text
        print(docText)


        text_array0 = docText.split()


        #Cropping uploaded prescription
        # cropped_name = './cut/crop'+ext
        cropped_name="crop"+ext   
        # im = Image.open('./fromfrontend/'+imagename)
        im = Image.open('media/'+imagename)

        height,width=im.size

        im.crop((0, height*.30, width, height+20)).save("media/"+cropped_name, quality=95) #cropped name can be path as well


        FOLDER_PATH = r'media/' #folderpath
        IMAGE_FILE = cropped_name
        FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

        with io.open(FILE_PATH, 'rb') as image_file:
            content = image_file.read()

        image = vision_v1.types.Image(content=content)
        response = client.document_text_detection(image=image)

        docText2 = response.full_text_annotation.text
        print(docText2)

        text_array = docText2.split()
        # print(text_array)
        try:
            n=text_array0.index("Dr")
            print(n)
            drname= text_array0[n+1:n+3]
            print(drname)
        except:
            res="No Dr name found."
            print(res)
        try:
            m=text_array0.index("Date")
            date= text_array0[m+1:m+4]
        except:
            res2="No date found."
            print(res2)

        UID=request.session['uid']
        data= pd.read_csv("names.csv")
        name_of_meds=data['Medicine_Name'].tolist()

        medi, sell_type, price, lqty, qty = [], [], [], [], []
        for i in text_array:
            if len(i)<3:
                continue
            else:
                value=difflib.get_close_matches(i, name_of_meds,1, 0.8)
                print(value)
                for j in value:
                    if j !=None or j !="":
                        indexincsv=name_of_meds.index(j)
                        count=0
                        with open('New_sample.csv', 'r') as f:
                            csv_reader = csv.reader(f)
                            for row in csv_reader:
                                if count ==indexincsv+1:  
                                    quan_left = int(dict(database.child("Medicine").child(row[0]).get().val())["Quantity"])
                                    medi.append(row[0])
                                    sell_type.append(row[2])
                                    price.append(row[5][4:])
                                    lqty.append(quan_left)
                                    qty.append(1)
                                    # database.child("Users").child(UID).child("Cart").child(row[0]).set({"Quantity":"1"})
                                    # # database.child("Medicines").child(row[0]).child("temp").

                                    # noofmeets = int(dict(database.child("Medicine").child(row[0]).get().val())["Temp"]) + 1
                                    # database.child("Medicine").child(row[0]).update({"Temp": noofmeets})
                                elif count>indexincsv:
                                    break
                                count=count+1
        delete = default_storage.delete(imagename)
        delete = default_storage.delete(cropped_name)
        combilis = zip(medi, sell_type, price, qty, lqty)
        cart_dct = {"medi": medi, "sell_type": sell_type, "price": price, "qty":qty}
        request.session["cart"] = cart_dct
        presc_link = storage.child("Prescripton").child(request.session["uid"]).get_url(None)
        return render(request,'cart.html',{"data":combilis, "presc_link": presc_link})
    return render(request,'upload-prescription.html')
    
def cart(request):
    UID=request.session['uid']
    cart = list(database.child("Users").child(UID).child("Cart").shallow().get().val())
    qty_list = dict(database.child("Users").child(UID).child("Cart").get().val())
    data= pd.read_csv("New_sample.csv")
    name_of_meds=data['Medicine_Name'].tolist()
    medi, sell_type, price, lqty, qty, presc_req = [], [], [], [], [], []
    for j in cart:
        if j !=None or j !="":
            indexincsv=name_of_meds.index(j)
            count=0
            with open('New_sample.csv', 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if count ==indexincsv+1:  
                        quan_left = int(dict(database.child("Medicine").child(row[0]).get().val())["Quantity"])
                        medi.append(row[0])
                        presc_req.append(row[1])
                        sell_type.append(row[2])
                        price.append(row[5][4:])
                        qty_left=int(dict(database.child("Medicine").child(row[0]).get().val())["Quantity"])
                        temp=int(dict(database.child("Medicine").child(row[0]).get().val())["Temp"])
                        lqty.append(min(qty_left-temp,5))
                        qty.append(qty_list[j]["Quantity"])
                    elif count>indexincsv:
                        break
                    count=count+1
    if "Prescription Required" in presc_req:
        prescreq = True
    combilis = zip(medi, sell_type, price, qty, lqty, presc_req)
    return render(request,"cart.html", {"presc_req": prescreq, "data": combilis, "manual": True})

def placeOrder(request):
    if request.method =='POST':
        name=request.POST.get('name')
        address=request.POST.get('address')
        phoneNo = request.POST.get("phoneNo")
        mode = request.POST.get('mode')
        presc_req = request.POST.get("presc_req")
        total = request.POST.get("total")
        email = request.POST.get("email")
        from datetime import date
        today = date.today()
        d1 = today.strftime("%d_%m_%Y")
        # print(name, address, phoneNo, mode, presc_req)
        if mode=="manual":
            if (presc_req):
                file = request.FILES['FileUpload']
                print(file)
                cart = dict(database.child("Users").child(request.session["uid"]).child("Cart").child().get().val())
                print(cart)
                data = {"Address":address, "Name":name, "FileLink": "None","Payment": "COD", "Status": "Not Verified", "Phone": phoneNo, "Scan": 0, "Total": total, "Email": email, "Date": d1}
                database.child("Users").child(request.session["uid"]).child("Orders").child("details").push(data)
            else:
                data = {"Address":address, "Name":name, "Payment": "COD", "Status": "Not Verified", "Phone": phoneNo, "Scan": 0, "Total": total, "FileLink": "None", "Email":email, "Date": d1}
                x = database.child("Users").child(request.session["uid"]).child("Orders").push(data)
                print(x)
                
                dict1 = {"data": "x", "data2": ["1", "2", "3"], "data3": 5}
                pdf = render_to_pdf('invoice.html', dict1)
                ref = storage.child("Invoice").child(request.session["uid"]+"_"+x["name"]).put("prescription.pdf")

                invoicelink = storage.child("Invoice").child(request.session["uid"]+"_"+x["name"]).get_url(None)
                data = {"InvoiceLink" : invoicelink, "UID":request.session["uid"]}
                database.child("AdminV").child("Veri").child(x["name"]).set(data)
        else:
            presc_link = request.POST.get("presc_link")
        return render(request, "Home.html")