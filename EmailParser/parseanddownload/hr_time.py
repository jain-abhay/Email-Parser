from dateutil.parser import *
from datetime import date
import datetime
import re

#This function tries finding the time that is in the given lines
def get_time(time_lines):
    #Final list to be returned
    time_list = []
    for line in time_lines:
        k = re.search(r' \d+[-| |(to)|\d|(am)|(pm)|(AM)|(PM)|:]*[a|p|A|P][m|M]',line[0])
        try:
            time_list.append((k.group(0),line[1]))
        except:
            continue
    return time_list


#This finds the 
def get_date_month(text, email_date,month):
    year = email_date.year
    if month+1 < email_date.month:
        year = year+1
    mon = ['January','February','March','April','May','June',
           'July','August','September','October','November','December']
    day = re.search(r'\d+',text)
    try:
        return day[0]+' '+mon[month]+' '+str(year)
    except:
        return mon[month]+' '+str(year)

def get_date_day(text, email_date, day):
    mon = ['January','February','March','April','May','June',
           'July','August','September','October','November','December']
    value = email_date.weekday()
    value = value - day
    if value < 0:
        value+=7
    if 'next' in text.lower():
        value+=7
    today = email_date+datetime.timedelta(days=value)
    return str(today.day)+' '+mon[today.month]+' '+str(today.year)

def get_date(date_lines, email_date):
    date_list = []
    for line in date_lines:
        #try:
        #    date_list.append((parse(line[0]),line[1]))
        #except:
        month = ['jan','feb','mar','apr','may','jun',
                   'jul','aug','sep','oct','nov','dec']
        day = ['monday','tuesday','wednesday','thrusday',
               'friday','saturday','sunday']
        for key in day+month:
            if key in line[0].lower():
                break
        else:
            break
        if key in month:
            date_list.append((get_date_month(line[0],email_date,month.index(key)),line[1]))
        else:
            date_list.append((get_date_day(line[0],email_date,day.index(key)),line[1]))
    return date_list

#Returns the lines which have the keywords
def get_info(lines,keyword):
    line_get_info = []
    for line in lines:
        for word in keyword:
            if word in line[0].lower():
                line_get_info.append(line)
                break
    return line_get_info


#Generates the lines from the text
def get_lines(text):
    #Required changes to text for splitting
    text = text.replace('Dr. ','Dr ')
    text = text.replace('Prof. ','Prof ')
    text = text.replace('Mr. ','Mr ')
    text = text.replace('Mrs. ','Mrs ')
    text = text.replace('  ',' ')
    #Generating lines by spliting at ;,. and \n
    temp_line = re.split(';|\. |\n|\*',text)
    #List containing lines
    lines = []
    #Used to add the line number
    i = 0
    for line in temp_line:
        #Doing the required changes to text
        line = line.replace('Dr ','Dr. ')
        line = line.replace('Prof ','Prof. ')
        line = line.replace('Mr ','Mr. ')
        line = line.replace('Mrs ','Mrs. ')
        lines.append((line.strip(),i))
        i+=1
    return lines
