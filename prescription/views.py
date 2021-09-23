from django.shortcuts import render
import os
import pyrebase
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv('\.env')
from django.http.response import HttpResponse
import pandas as pd
from django.core.files.storage import FileSystemStorage

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
        name=request.POST.get('name')
        print(name)
        return HttpResponse('')

def inc_cart_qty(request):
    if request.method =='POST':
        UID= request.session['uid']
        med_name=request.POST.get('meds')
        quantity=request.POST.get('no_units')
        
        database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":quantity})
                                                                        # quantity lena chahiye yaa +1 ye doubt hai 

        noofmeets = int(dict(database.child("Medicine").child(med_name).get().val())["Temp"]) + 1
        database.child("Medicine").child(med_name).update({"Temp": noofmeets})

        return HttpResponse('')

def change_invent_qty(request):
    if request.method =='POST':
        UID= request.session['uid']
        med_name=request.POST.get('meds')
        quantity=request.POST.get('no_units')
        
        # database.child("Users").child(UID).child("Cart").child(med_name).set({"Quantity":quantity})
                                                                        # quantity lena chahiye yaa +1 ye doubt hai 

        # noofmeets = int(dict(database.child("Medicine").child(med_name).get().val())["Temp"]) + 1
        database.child("Medicine").child(med_name).update({"Quantity": quantity})

        return HttpResponse('')



def product(request):

    medname=request.POST.get("medicine_name")
    # data1=[]
    # classa = "Allegra 180mg Tablet"
    # df=pd.read_csv('New_Sample.csv')
    # newdf=df.query('Medicine_Name == "{0}"'.format(classa))
    # print(newdf)
    # data_array=newdf.values[0]
    # print(data_array)


    return render(request,"login.html")

def read_presc(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        

    # return render(request, 'cart.html')

        from PIL import Image
        import os, io
        from google.cloud import vision_v1
        import difflib
        import csv
        from google.cloud.vision_v1 import types
        import pathlib

        #getting file from front end
        imagename='no3.png'
        
        ext = pathlib.Path(imagename).suffix

        #Reading prescription photo for dr and date tag
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ascendant-choir-326117-f6d97fe48d5c.json'
        client = vision_v1.ImageAnnotatorClient()

        FOLDER_PATH = r''
        # IMAGE_FILE = './fromfrontend/'+imagename
        IMAGE_FILE = imagename
        FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

        with io.open(FILE_PATH, 'rb') as image_file:
            content = image_file.read()


        image = vision_v1.types.Image(content=content)
        response = client.document_text_detection(image=image)

        docText = response.full_text_annotation.text
        print(docText)


        text_array0 = docText.split();


        #Cropping uploaded prescription
        # cropped_name = './cut/crop'+ext
        cropped_name="crop"+ext
        # im = Image.open('./fromfrontend/'+imagename)
        im = Image.open(imagename)

        height,width=im.size

        im.crop((0, height*.30, width, height+20)).save(cropped_name, quality=95)


        #reading cropped prescription for meds
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ascendant-choir-326117-f6d97fe48d5c.json'
        client = vision_v1.ImageAnnotatorClient()

        FOLDER_PATH = r''
        IMAGE_FILE = cropped_name
        FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

        with io.open(FILE_PATH, 'rb') as image_file:
            content = image_file.read()

        image = vision_v1.types.Image(content=content)
        response = client.document_text_detection(image=image)

        docText2 = response.full_text_annotation.text
        print(docText2)

        text_array = docText2.split();
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

        # UID=request.session['UID']
        UID="Rsz5MPwnYhbpNV6D42qorchrvBH3"
        data= pd.read_csv("names.csv")
        name_of_meds=data['Medicine_Name'].tolist()
        print(text_array)


        meds=[]
        meds_details=[]

        for i in text_array:
            if len(i)<3:
                continue
            else:
                value=difflib.get_close_matches(i, name_of_meds,1, 0.8)

                # print(name_of_meds)
                print(value)
                for j in value:
                    if j !=None or j !="":
                        print(name_of_meds.index(j))
                        indexincsv=name_of_meds.index(j)
                        dic={
                            j:indexincsv
                        }
                        meds.append(dic.copy())
                        count=0
                        with open('New_sample.csv', 'r') as f:
                            csv_reader = csv.reader(f)
                            for row in csv_reader:
                                if count ==indexincsv+1:  
                                    info=[row[0],row[2],row[5]] 
                                    meds_details.append(info)

                                    database.child("Users").child(UID).child("Cart").child(row[0]).set({"Quantity":"1"})
                                    # database.child("Medicines").child(row[0]).child("temp").

                                    noofmeets = int(dict(database.child("Medicine").child(row[0]).get().val())["Temp"]) + 1
                                    database.child("Medicine").child(row[0]).update({"Temp": noofmeets})

                                elif count>indexincsv:
                                    break
                                count=count+1

        print(meds)
        print(meds_details)

        return render(request,'homepage.html',{"data":meds_details})
    return render(request,'upload-prescription.html')
