from django.shortcuts import render
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64,time,re,csv,email,datetime,googleapiclient
from bs4 import BeautifulSoup as bs
import dateutil.parser as parser
from datetime import datetime
#from .models import TalksData
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import hashlib


def getemail(number):
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('/parseanddownload/storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/parseanddownload/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'INBOX'

