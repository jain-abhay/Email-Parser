from nltk.parse import CoreNLPParser
from .hr_time import *
from itertools import combinations
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import re
from fuzzysearch import find_near_matches

def get_nertag(text):
    ner_tagger = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz','stanford-ner.jar',encoding='utf-8')
    tokenized_text = word_tokenize(text)
    classified_text = ner_tagger.tag(tokenized_text)
    possible_speakers = ['']
    organizations = set()
    persons = set()
    locations = set()
    for i in classified_text:
        if i[1]=='ORGANIZATION':
            organizations.add(i[0])
        if i[1]=='LOCATION' or i[1]=='STATE_OR_PROVINCE':
            organizations.add(i[0])
        if i[1]=='PERSON':
            persons.add(i[0])
    for i in classified_text:
        if i[1]=='PERSON':
            possible_speakers[len(possible_speakers)-1]+=' '
            possible_speakers[len(possible_speakers)-1]+=i[0]
        elif possible_speakers[len(possible_speakers)-1]!='':
            possible_speakers.append('')
    try:
        possible_speakers.remove('')
    except:
        pass
    for i in possible_speakers:
        i = i.strip()
        i = i.replace('*','')
        i = i.replace(';','')
        i = i.replace('!','')
    possible_speakers = list(set(possible_speakers))
    #speaker_temp = [set(j.split()) for j in possible_speakers]
    #speakers = set()
    #for i in speaker_temp:
    #    for j in speaker_temp:
    #        if i!=j and i>j and i not in speakers:
    #            speakers.append(i)
    #speakers = list(speakers)
    return (list(organizations),list(persons),possible_speakers,locations)

def get_speaker_salutaion(text, persons, speakers):
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    text = text.split()
    pos_tag_list = list(pos_tagger.tag(text))
    for i in range(len(pos_tag_list)-1):
        if pos_tag_list[i][1]=='NNP' and pos_tag_list[i][0] not in persons:
            if pos_tag_list[i+1] in persons:
                for speak in speakers:
                    if pos_tag_list[i+1] in speak:
                        speak = pos_tag_list[i]+' '+speak
                        break
    return speakers

def speaker_indexing(speakers, lines):
    speaker_index = []
    for i in range(len(lines)):
        for speak in speakers:
            if len(find_near_matches(speak.lower(),lines[i][0].lower(), max_l_dist=1))!=0:
                speaker_index.append((speak,i))
    return speaker_index

def find_title(text):
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    lines = re.split(r'\. | on |\n',text)
    lines = [(lines[j].strip(),j) for j in range(len(lines))]
    #keyword = ['date','monday','tuesday','wednesday','thrusday','friday',
    #           'saturday','sunday','january','february','march','april','may','june','july',
    #           'august','september','october','november','december',
    #           ' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9',' 0',
    #           '-1','-2','-3','-4','-5','-6','-7','-8','-9','-0']
    keyword = ['talk','seminar','speak','session','workshop']
    title_lines = get_info(lines,keyword)
    #for line in title_lines:
    #    pos_tag_list = list(pos_tagger.tag(line[0].split()))
    #    verb_set = [j[1] for j in pos_tag_list]
    #    if (('VB' in verb_set) or ('VBD' in verb_set) or ('VBN' in verb_set)):
    #        line.append(0)
    #    else:
    #        line.append(1)
    return title_lines


def find_title_mentioned(title_lines):
    titles = []
    for line in title_lines:
        pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
        pos_tag_list = list(pos_tagger.tag(line[0].split()))
        m = len(pos_tag_list)
        preposition_list = []
        for j in range(m):
            if pos_tag_list[j][0]=='on':
                preposition_list.append(j)
        preposition_list.append(m)
        preposition_combinations = list(combinations(preposition_list,2))
        for j in preposition_combinations:
            word_list = [j[0] for j in pos_tag_list]
            title = ' '.join(word_list[j[0]+1:j[1]+1])
            x = 0
            for k in range(len(title)):
                if title[k].lower().isalpha()==True:
                    x = k
                    break
            title = title[m:]
            titles.append((title, line[1]))
        preposition_list = []
        for j in range(m):
            if pos_tag_list[j][0]=='is':
                preposition_list.append(j)
        preposition_list.append(m)
        preposition_combinations = list(combinations(preposition_list,2))
        for j in preposition_combinations:
            word_list = [j[0] for j in pos_tag_list]
            title = ' '.join(word_list[j[0]+1:j[1]+1])
            x = 0
            for k in range(len(title)):
                if title[k].lower().isalpha()==True:
                    x = k
                    break
            title = title[x:]
            titles.append((title, line[1]))
    return titles
