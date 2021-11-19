from django.shortcuts import render
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64,time,re,csv,email,datetime,googleapiclient
from bs4 import BeautifulSoup as bs
import dateutil.parser as parser
from datetime import datetime
from .models import TalksData
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .getallseminars import *
from .execution import *
import hashlib,os

# Create your views here.
@csrf_exempt
def show_the_db(request):
    try:
        all_talks=TalksData.objects.all()
        return render(request,'showdata.html',{'talks':all_talks})
    except Exception as e:
        print(e)
        return render(request,'uploadfromgmail.html',{})

@csrf_exempt
def clear_db(request):
    try:
        obj=TalksData.objects.all()
        obj.delete()
        # createcsv()
        return HttpResponse("Database Cleared")
    except:
        return HttpResponse("Not able to delete or empty")

@csrf_exempt
def upload_from_gmail(request):

    if "GET" == request.method:
        return render(request, 'uploadfromgmail.html', {})
    else:

        number=10
        alltalkdict=getemail(number)
        for i in alltalkdict:
            print("in")
            try:
                # print(3)
                a=TalksData.objects.get(Subject=i['Subject'],Sender=i['Sender'],DateofEmail=i['Date'],Message_body=i['Message_body'])
            except:
                body=i['Message_body']
                if ("mathematics discipline seminar" in i['Subject'].lower()):
                    try:
                        print(1)
                        print("/parseanddownload/attachments/"+hashlib.sha224(body.encode('ASCII')).hexdigest()+".pdf")
                        finaldict=get_mathematics_data(os.getcwd()+"/parseanddownload/attachments/"+hashlib.sha224(body.encode('ASCII')).hexdigest()+".pdf")
                        print(2)
                        # for i in finaldict:
                        #         if not str(i).strip():
                        #             finaldict[i]="N.A."
                        TalksData.objects.create(Sender=i['Sender'],Subject=i['Subject'],DateofEmail=i['Date'],Message_body=body,Speaker=finaldict['Speaker'],Topic=finaldict['Topic'],Time=finaldict['Time'],DateofWorkshop=finaldict['Date'],Venue=finaldict['Venue'])
                        # createcsv()
                    except Exception as e:
                        print(e)
                else:
                    try:
                        finallistofdict=mail(i)
                        for finaldict in finallistofdict:
                            # for i in finaldict:
                            #     if not str(i).strip():
                            #         finaldict[i]="N.A."
                            Speaker,Topic,DateofWorkshop,Venue,Time=finaldict
                            TalksData.objects.create(Sender=i['Sender'],Subject=i['Subject'],DateofEmail=i['Date'],Message_body=body,Speaker=Speaker,Topic=Topic,DateofWorkshop=DateofWorkshop,Venue=Venue,Time=Time)
                        # createcsv()
                    except Exception as e:
                    	print(e)

        try:
        	all_talks=TalksData.objects.all()
        	return render(request,'showdata.html',{'talks':all_talks})
        except Exception as e:
        	return render(request,'uploadfromgmail.html',{})


# def createcsv():
#     a=open('database.csv','wb',newline='')
#     writer=csv.writer(a)
#     allobj=TalksData.objects.all()
#     writer.writerow(['Sender','Speaker','Topic','Date','Time','Venue'])
#     for i in allobj:
#         row=[]
#         row.append(i.Sender)
#         row.append(i.Speaker)
#         row.append(i.Topic)
#         row.append(i.Date)
#         row.append(i.Time)
#         row.append(i.Venue)
#         writer.writerow(row)