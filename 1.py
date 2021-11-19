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
def data_encoder(text):
    if len(text)>0:
        message = base64.urlsafe_b64decode(text)
        message = str(message, 'utf-8')
        # message = quopri.decodestring(message).decode('utf8')
        message = email.message_from_string(message)
    return message

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

unread_msgs = GMAIL.users().messages().list(
    userId='me', labelIds=[label_id_one, label_id_two]).execute()


mssg_list = unread_msgs['messages']
final_list = []
ui = 0

for mssg in mssg_list[:10]:
    temp_dict = {}
    
    m_id = mssg['id']  # get id of individual message
    message = GMAIL.users().messages().get(
        userId=user_id, id=m_id).execute()  # fetch the message using API
    payld = message['payload']  # get payload of the message
    # print(message)
    try:
        headr = payld['headers']  # get header of the payload

        message2 = GMAIL.users().messages().get(userId=user_id, id=m_id,
                                                format='raw').execute() 

    
        content=message
        if "data" in content['payload']['body']:
            message = content['payload']['body']['data']
            message = data_encoder(message)
        elif "data" in content['payload']['parts'][0]['body']:
            message = content['payload']['parts'][0]['body']['data']
            message = data_encoder(message)
        else:
            message=""

        if '</html>' in str(message):
            soup=bs(message,'html.parser')
            s=soup.find_all('p')
            
            # print(s)
            t="".join([i.text for i in s])
        else:
            t=str(message)
        print(t)

        
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
        temp_dict('Message_body')=t

        ui = ui + 1
        final_list.append(temp_dict)

        # This will mark the messagea as read
        GMAIL.users().messages().modify(userId=user_id, id=m_id,
                                        body={'removeLabelIds': ['UNREAD']}).execute()
    except Exception as e:
        print(e)

print("Total messaged retrived: ", str(len(final_list)))


with open('CSV_NAME.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['Sender', 'Subject', 'Date', 'Message_body']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()
    for val in final_list:
        writer.writerow(val)

