import re
import hr_time    

    
def searchforvenue(message_body):
    all_lines=get_lines(message_body)
    s=[]
    for i in range(all_lines[-1][1]+1):
        s.append((re.findall(r'(\d{0,3}\s{0,1}(auditorium|Audi |audi$|jb|ab|jasubhai\sauditorium|block|room|academic\sblock){0,1}\s{0,1}(\d\/\d{3}){0,1})',all_lines[i][0])[0][0],i))
    return s
message_body="""Audi."""
print(searchforvenue(message_body))