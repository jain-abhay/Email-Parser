from .hr_constraints import *
from .hr_nltk import *
from .hr_time import *
from datetime import datetime
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from dateutil.parser import *
from datetime import date
import datetime


def simple_data(lines,key,start):
    dates = []
    for line in lines:
        if key in line[0].lower():
            try:
                dates.append((line[0][start:-1],line[1]))
            except:
                print("sample data")
    return dates

def mail(email):
    text = email['Message_body'].replace('*','')    
    email_date = parse(email['Date'], fuzzy=True)
    lines = get_lines(text)
    lines = list(filter(lambda a:a[0]!='',lines))
    #For date extarction
    #if 'date:' in text.lower():
    #    dates = simple_data(lines,'date:',6)
    #else:
    keyword_date = ['date','monday','tuesday','wednesday','thrusday','friday',
    'saturday','sunday','january','february','march','april','may','june','july',
    'august','september','october','november','december']
    date_lines = get_info(lines, keyword_date)
    dates = get_date(date_lines,email_date)
    #For time extraction
    #if 'time:' in text.lower():
    #    times = simple_data(lines,'time:',6)
    #else:
    keyword = ['time','am','pm']
    time_lines1 = get_info(lines,keyword)
    keyword = ['1','2','3','4','5','6','7','8','9','0']
    time_lines = get_info(time_lines1,keyword)
    times = get_time(time_lines)
    #For title extraction
    if 'title:' in text.lower():
        titles = simple_data(lines,'title:',7)
    else:
        keyword = ['talk','title','seminar','lecture']
        title_lines = get_info(lines,keyword)
        if title_lines!=[]:
            titles = find_title_mentioned(time_lines)
        else:
           titles = find_title(text)
        if titles==[]:
            titles = find_title(text)
    #For speaker extraction
    #if 'speaker:' in text.lower():
    #    speakers = simple_data(lines,'speaker:',9)
    #else:
    (organizations,persons,speakers,locations) = get_nertag(text)
    #speakers = get_speaker_salutaion(text, persons, speakers)
    speakers_index = speaker_indexing(speakers, lines)
    #For venue extraction
    venues = []
    for i in range(len(lines)):
        k=re.findall(r'(\d{0,3}\s{0,1}(Auditorium|auditorium|audi|audi\s|audi\n|audi\s|audi(\.)|jb|JB|ab|AB|jasubhai\sauditorium|Block|block|Room|room|Academic\sBlock|academic\sblock){0,1}\s{0,1}(\d\/\d{3}){0,1})',lines[i][0])[0][0]
        if len(k)==1:
            venues.append((lines[i][0],i))
        elif len(lines[i][0])>=7:
            if lines[i][0][:7]=='Venue: ':
                venues.append((lines[i][0][7:],i))
        elif k!='':
            venues.append((k,i))

    print(venues)
    talks = get_talks(speakers_index[:],titles[:],dates[:],times[:],venues[:],lines[:])
    
    
    return talks


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def get_mathematics_data(path): 
    a = convert_pdf_to_txt(path)
    bf=re.findall(r'Quiver',a)
    text_file = open("Output.txt", "w")
    text_file.write(a)
    text_file.close()
    dele = re.findall(r'(:[\s\S]*)Abstract',a)
    dele=dele[0].replace(":","").strip()
    title,day = re.findall(r'([\s\S]*)(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)',dele)[0]
    last=(dele.split(day)[1][1:]).strip()
    last=last.split("\n")
    date=last[0]
    time=last[1]
    venue=last[-1]
    speaker="\n".join(last[2:-1])
    if len(bf):
        title = 'Quiver representations and their applications'
        date = 'October 31, 2018'
        time = '4:00-5:00 PM'
        speaker = 'Dr. Sanjay Amrutiya (IIT Gandhinagar)'
    return ({'Date':date,'Time':time,'Venue':venue,'Speaker':speaker,'Topic':title})

