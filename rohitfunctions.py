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
    return ({'Date':date,'Time':time,'Venue':venue,'Speaker':speaker,'Title':title})
