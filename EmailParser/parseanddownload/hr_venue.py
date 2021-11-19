import re

class VenueSearch():

    keywords=['venue','Venue','place','Place']

    def regexvenue(self,message):
        # subject=message['subject']
        # message_body=message['message_body']
        # alllines=self.get_lines(message_body)
        alllines=self.get_lines(message)
        # print(alllines)
        venue_possibilities=[]
        for line in alllines:
            for keyword in self.keywords:
                # print(keyword)
                if keyword in line[0].lower():
                    venue_possibilities.append(line)
        return venue_possibilities

        

    def get_lines(self,message_body):
        temp_line = message_body.split('\n')
        lines = []
        i = 0
        for line in temp_line:
            if '.' in line:
                f_lines = line.split('.')
                for f_line in f_lines:
                    f_line=f_line.strip()
                    if len(f_line):
                        lines.append((f_line,i))
                        i+=1
            else:
                line=line.strip()
                if len(line):
                    lines.append((line,i))
                    i+=1
        return lines
    
    venuekeywords=['Academic Block','AB','Audi','Auditorium','Block','JB','Jasubhai']
    final_venues=[]
    
    def searchforvenue(self,message_body):
        self.venue_possibilities=regexvenue(message_body)
        if len(self.venue_possibilities):
            
        else:
            all_lines=self.get_lines(message_body)
            
    def searchforvenueinalist(self, linelist):
        for lines in self.venue_possibilities:
                x=re.findall(r'([A][B])?( )+\d\\\d\d\d',line[0])
                if len(x):
                    self.final_venues.append((x,line[1]))
                else:
                    x=re.findall(r'\d\d\d',line[0])
                    if len(x):
                        
                if ('Jasubhai Auditorium' or 'Jasubhai Audi' or 'JB') in line[0]:
                    self.final_venues.append(('Jasubhai Audi',line[1]))
                 


    


message_body="""Dear All,

Dr. Prakash Saivasan is a faculty candidate in CSE discipline and he will be visiting us on January 8,9 2018. The details of his research and teaching sessions are as follows. 

Research Seminar:  Regular abstractions with applications to Infinite state verification
Time/Date: 2:30 pm to 3:30 pm, Jan 8 (Tue)
Venue: 5/202

Abstract: 
Recursive programs  even over finite data domains are infinite state due to the unboundedness of the call stack. While sequential recursive programs can be modelled and verified via pushdown systems, verification in the presence of concurrency, which is undecidable in general, remains an interesting  and challenging problem.  The focus of my research so far has been to  address this problem via different techniques: under-approximations, accelerations and via regular abstractions. In this talk I will present one of our result on regular abstractions.  

A regular abstraction is the approximation of an infinite state system as a finite automaton.  For instance, one may approximate the behaviors (as a language) of a recursive program/pushdown system by its downward closure (i.e.  the collection of all subwords of words in the language), this is always a regular language. One may also disregard the order of letters in the words and consider the Parikh-image of a language. Again for recursive programs/ pushdown systems, this is representable by a finite state automaton.  

I will explain the main ideas behind our results  on computing regular abstractions  for automata equipped with a counter. While such representations for pushdown systems  involves an exponential blowup, we will see that the situation is significantly better for counter systems.  It is polynomial for both upward and downward closures and quasi-polynomial for Parikh-image abstraction.  

I will then show how to use the above result to carry out verification of quantitative properties for  procedural programs.  Our Quantitative logic provides the ability to express arithmetic constraints over the execution times of procedure invocations. In this logic one may express properties  such as “within the execution of each invocation of a procedure P, the time spent in executing invocations of procedures Q and R is less than 15%”.

Time permitting, I will also explain a second application of our result: in deciding the control state reachability problem for an under-approximation (bounded-stage runs) of  concurrent recursive programs communicating via shared memory.


Teaching seminar: Pumping Lemma
Time/ Date: 10 am - 11 am, Jan 9 (Wed)
Venue: 6/202
"""

newmsgbody="The venue for this seminar is 7/202"
venuesearch=VenueSearch()
# venues=venuesearch.regexvenue(message_body)
venues=venuesearch.regexvenue(newmsgbody)
print(venues)

