import re

def extractcse(msg_body):
	l=re.findall(r'Title:.*\n',msg_body)
	m=re.findall(r'Speaker:.*\n',msg_body)
	n=re.findall(r'Date:.*\n',msg_body)
	o=re.findall(r'Time:.*\n',msg_body)
	p=re.findall(r'Venue:.*\n',msg_body)
	try:
		l_final = l[0][7:-1]
	except:
		l_final = "NA"
	try:
		m_final = m[0][9:-1]
	except:
		m_final = "NA"
	try:
		n_final = n[0][6:-1]
	except:
		n_final = "NA"
	try:
		o_final = o[0][6:-1]
	except:
		o_final = "NA"
	try:
		p_final = p[0][7:-1]
	except:
		p_final = "NA"
	return l_final,m_final,n_final,o_final,p_final

msg_body="""Dear all,

We are glad to announce the next seminar of CSE seminar series of this semester on Wednesday, 4th April 2018 by Tom Glint Issac, Ph.D., Computer Science and Engineering. The details of the seminar are as follows:

Title: Trip Report on GIAN COURSE + SCEC 17 + HiPC 17

Speaker: Tom Glint Issac, Ph.D., CSE

Date: 4th April 2018 


Abstract:
During the winter break of 2017, I attended a GIAN course, a workshop, and a conference.

The GIAN Course titled Emerging Computational Devices, Architectures and Systems- dealt with the following topics:  Emerging logic and memory devices; Circuit/Architecture design using Emerging Logic and Memory devices; Processor-in-Memory Architectures using emerging devices; Neuromorphic and Brain Inspired Computational Models; Computing Using Coupled Oscillator Systems; and Other Emerging Computational Models.

The Workshop on Software Challenges to Exascale Computing (SCEC 17) was focused on sharing the challenges faced by large problems that require HPC hardware to solve. The workshop had software and hardware perspectives.

The IEEE International Conference on High-Performance Computing (HiPC 2017) was a forum for researchers to present their work on areas of algorithms, system software, and architectures. It was also a place where vendors can showcase their latest product and services in the HPC domain.

In this talk, I would like to give a comprehensive presentation on the important problems in Computer Systems that people are trying to solve, a sample workflow involved with systems research, and my overall experience during the trip.  

Please mark this seminar on your calendar.

Thanks,
Ananya"""

l_final,m_final,n_final,o_final,p_final = extractcse(msg_body)
print(l_final)
print(m_final)
print(n_final)
print(o_final)
print(p_final)