from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup as bs
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
import email

def removetrash(subject,body):
	keywords = ['hack','talk','seminar','lecture series', 'lecture', 'mathematics discipline seminar', 'CSE discipline seminar']
	for k in keywords:
		if k in subject.lower():
			return True
		elif k in body.lower():
			return True

def GetAttachments(service, user_id, msg_id, prefix=""):

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data=part['body']['data']
                else:
                    att_id=part['body']['attachmentId']
                    att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                    data=att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = prefix+part['filename']

                with open(path, 'wb') as f:
                    f.write(file_data)
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)

def removeforwadedmsgs(email_body):
    s=email_body.split("---------- Forwarded message ---------\n")
    s=s[-1]
    s=s.split("\n")
    if s[0][:6]=="From: ":
        s=s[1:]
        if s[0][:6]=="Date: ":
            s=s[1:]
            if s[0][:9]=="Subject: ":
                s=s[1:]
                if s[0][:4]=="To: ":
                    s=s[1:]
                    if s[0][:4]=="Cc: ":
                        s=s[1:]
    s="\n".join(s)
    return s 

def forwardedmsgsv2(email_body):
    email_body=email_body.split("@")
    email_body=email_body[-1]
    email_body=email_body.split(".")
    email_body=".".join(email_body[1:])
    return email_body


def filter_email(email_body):
    email_body=email_body.replace(">","")
    email_body=email_body.replace("<","")
    print(email_body)
    email_body=forwardedmsgsv2(email_body)
    print(email_body)
    return email_body

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_id_one = 'INBOX'
label_id_two = 'INBOX'

def data_encoder(text):
    if len(text)>0:
        message = base64.urlsafe_b64decode(text)
        message = str(message, 'utf-8')
        # message = quopri.decodestring(message).decode('utf8')
        message = email.message_from_string(message)
    return message

unread_msgs = GMAIL.users().messages().list(
    userId='me', labelIds=[label_id_one, label_id_two]).execute()


mssg_list = unread_msgs['messages']
final_list = []

for mssg in mssg_list[:20]:
    temp_dict = {}
    
    m_id = mssg['id']  # get id of individual message
    message = GMAIL.users().messages().get(
        userId=user_id, id=m_id).execute()  # fetch the message using API
    payld = message['payload']  # get payload of the message

    try:

        headr = payld['headers']  # get header of the payload

    
        content=message
        if "data" in content['payload']['body']:
            message = content['payload']['body']['data']
            message = data_encoder(message)
        elif "data" in content['payload']['parts'][0]['body']:
            message = content['payload']['parts'][0]['body']['data']
            message = data_encoder(message)
        elif "data" in content['payload']['parts'][0]['parts'][0]['body']:
            message= content['payload']['parts'][0]['parts'][0]['body']['data']
            message = data_encoder(message)
        elif "data" in content['payload']['parts'][0]['parts'][0]['parts'][0]['body']:
            message= content['payload']['parts'][0]['parts'][0]['parts'][0]['body']['data']
            message = data_encoder(message)
        else:
            message=""

        if '</html>' in str(message):
            soup=bs(message,'html.parser')
            s=soup.find_all('p')
            t="".join([i.text for i in s])
        else:
            t=str(message)
        t=filter_email(t)
        print(t,"\n\n\n\n")
        temp_dict['Message_body']=t.replace('\n',' ')

        
        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
            else:
                pass

        for two in headr:  # getting the date
            if two['name'] == 'Date':
                msg_date = two['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)
            else:
                pass

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
            else:
                pass
        if (removetrash(msg_subject,t)):
        #print(temp_dict)
            final_list.append(temp_dict)
            GetAttachments(GMAIL, user_id, m_id, prefix="")
        

        GMAIL.users().messages().modify(userId=user_id, id=m_id,
                                        body={'removeLabelIds': ['UNREAD']}).execute()
    except Exception as e:
        print(e)

