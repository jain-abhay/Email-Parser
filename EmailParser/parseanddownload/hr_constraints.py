#import hr_time
#import hr_nltk
from nltk.parse import CoreNLPParser
import numpy as np

def get_sum_matrix(matrix):
    m_sum = 0
    for i in matrix:
        m_sum+=len(i)
    return m_sum

def scorer(title, speaker):
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    pos_tag_list = list(pos_tagger.tag(title[0].split()))
    s = 0
    for i in pos_tag_list:
        if 'NN' in i[1] or 'NP' in i[1]:
            s+=1
    return -s+abs(title[1]-speaker[1])*0.3

def get_probable_title(titles):
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    score = []
    for title in titles:
        pos_tag_list = list(pos_tagger.tag(title[0].split()))
        s = 0
        for i in pos_tag_list:
            if 'NN' in i[1] or 'NP' in i[1]:
                s+=1
        score.append((s,len(title[0]),title[0],title[1]))
    return max(score)

def get_talks(speakers, titles, dates, times, venues, lines):
    print("function start")
    talks = []
    speakers.sort(key=lambda x: x[1])
    titles.sort(key=lambda x: x[1])
    dates.sort(key=lambda x: x[1])

    times.sort(key=lambda x: x[1])
    venues.sort(key=lambda x: x[1])
    
    if len(titles)==0:
        return talks
    if len(speakers)==0:
        return talks
    
    matrix = []
    
    for speak in speakers:
        row = []
        for title in titles:
            row.append(scorer(title,speak))
        matrix.append(row)
    
    matrix = np.array([np.array(j) for j in matrix])
    m_max = matrix.max()
    m_min = matrix.min()
    matrix = list([list(j) for j in matrix])
    
    #First speaker handling
    mini = min(matrix[0])
    mini_i = [j for j in range(len(matrix[0])) if matrix[0][j]==mini][0]
    #temp_titles = [titles[j] for j in range(len(matrix[0])) if matrix[0][j]==mini]
    #matrix_pop_list = [j for j in range(len(titles)) if matrix[0][j]==mini]
    matrix_pop_list = [mini_i]
    #title = get_probable_title(temp_titles)
    title = titles.pop(mini_i)

    for j in matrix_pop_list:
        for k in range(len(speakers)):
            matrix[k].pop(j)
    print("first talk")
    talk = []
    talk.append(speakers[0][0])
    talk.append(title[0])#Text of title
    talk.append('')#Date
    talk.append('')#Venue
    talk.append('')#Time
    
    #title[3] is line number
    
    temp_dates = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in dates]
    temp_dates.sort(key=lambda x: x[2])
    
    try:
        talk[2] = temp_dates[0][0]
        dates_position = title[1]-temp_dates[0][1]
    except:
        pass
    
    temp_venues = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in venues]
    temp_venues.sort(key=lambda x: x[2])
    
    try:
        talk[3] = temp_venues[0][0]
        venues_position = title[1]-temp_venues[0][1]
    except:
        pass
    
    temp_times = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in times]
    temp_times.sort(key=lambda x: x[2])
    
    try:
        talk[4] = temp_times[0][0]
        times_position = title[1]-temp_times[0][1]
    except:
        pass
    
    print('first-talk',talk)

    talks.append(talk[:])

    print('talk append')
    matrix = np.array([np.array(j) for j in matrix])
    try:
        mmin = matrix.min()
    except:
        return talks
    ###############################################################
    #Positions have been determined
    print(dates)
    print(matrix)
    print('begining while')
    while(len(titles)>0 and mmin<0.1):
        print('entered while')
        talk = []

        matrix = np.array([np.array(j) for j in matrix])
        
        mmin = matrix.min()#minimum in matrix
        
        mmin_p = np.unravel_index(matrix.argmin(), matrix.shape)#position of mmin

        print(mmin,mmin_p)



        speaker = speakers[mmin_p[0]]
        
        matrix = list([list(j) for j in matrix])
        matrix_pop_list = [mmin_p[1]]

        for j in matrix_pop_list:
            for k in range(len(speakers)):
                matrix[k].pop(j)

        title = titles.pop(mmin_p[1])

        talk = []
        talk.append(speaker[0])
        talk.append(title[0])
        talk.append('')#Date
        talk.append('')#Venue
        talk.append('')#Time
        

        temp_dates = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in dates if title[1]-j[1]==dates_position]
        temp_dates.sort(key=lambda x: x[2])

        if temp_dates!=[]:
            talk[2] = temp_dates[0][0]
        else:
            temp_dates = [(j[0],j[1],(abs(title[1]-j[1])), -len(lines[j[1]])) for j in dates]
            temp_dates.sort(key=lambda x: x[2])
            if temp_dates!=[]:
                talk[2] = temp_dates[0][0]

        temp_venues = [(j[0],j[1],(abs(title[1]-j[1])), -len(lines[j[1]])) for j in venues if title[1]-j[1]==venues_position]
        temp_venues.sort(key=lambda x: x[2])

        if temp_venues!=[]:
            talk[3] = temp_venues[0][0]
        else:
            temp_venues = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in venues]
            temp_venues.sort(key=lambda x: x[2])
            print(temp_venues)
            if temp_venues!=[]:
                talk[3] = temp_venues[0][0]

        temp_times = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in times if title[1]-j[1]==times_position]
        temp_times.sort(key=lambda x: x[2])

        print(temp_times)

        if temp_times!=[]:
            talk[4] = temp_times[0][0]
        else:
            temp_times = [(j[0],j[1],(abs(title[1]-j[1]), -len(lines[j[1]]))) for j in times]
            temp_times.sort(key=lambda x: x[2])
            print(temp_times)
            if temp_times!=[]:
                talk[4] = temp_times[0][0]

        talks.append(talk)

        print(talks)


        matrix = np.array([np.array(j) for j in matrix])
        try:
            mmin = matrix.min()
        except:
            return talks
    return talks
