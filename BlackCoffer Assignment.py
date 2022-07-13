#!/usr/bin/env python
# coding: utf-8

# # Webscrapping and Saving

# In[2]:


import pandas as pd


# In[ ]:


from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[ ]:


df = pd.read_excel("C:\IIT BSc. Data Science and Programming\Internships\Input.xlsx")


# In[3]:


answer_df = pd.read_excel("C:\IIT BSc. Data Science and Programming\Internships\Output.xlsx")


# In[ ]:


df.head()


# In[ ]:


count = 0
url = 1


# In[ ]:


#webscrapping and saving articles as text files


for i in df['URL']:
    raw_request = Request(i)
    raw_request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0')
    raw_request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    resp = urlopen(raw_request) #opening url
    raw_html = resp.read() #reading the content
    soup = BeautifulSoup(raw_html, 'html.parser') #creating beautiful soup object
    count = count+1
    zeug = [x.get_text() for x in soup.find_all('div', attrs={'class': 'td-post-content'})]  
    #getting the required article which was under div tag with class td-post-content
    string = ''
    for i in zeug:
        string = i+string       #obtaining the article in a readable format
    
    #saving the file
    file = open(f'{url}.txt','w',encoding = 'utf-8') 
    file.write(string)
    file.close()
    url = url+1
    print(count)


# # Obtaining the list of stopwords (alternative approach: nltk.corpus)

# In[ ]:


#opening the stopwords file

file1 = open("C:\IIT BSc. Data Science and Programming\Internships\StopWords_GenericLong.txt",'r')


# In[ ]:


#reading the stopwords file provided in the google drive

stopwords = file1.readlines()


# In[ ]:


#obtaining a list of stopwords

general_stopwords_list = []
for i in stopwords:
    x = i.replace('\n','')
    general_stopwords_list.append(x)
general_stopwords_list[:5]


#  # Code for cleaning the text for all 150 links. Calculate Scores before last print statement

# In[4]:


import nltk
from nltk.corpus import stopwords
import re


# In[5]:


#defining function for obtaining necessary part of the text, removing spaces at beginning

def setup(txt):
    li = []
    for i in txt:
        x = i.split()
        li.append(x)
    subl = [subl for subl in li if len(subl)!=0 ]
    subl = subl[:-1]
    text = subl
    return text


# In[6]:


#code for cleaning (punctuations,converting to lower case, filtering stopwords )
def transform (text):
    review = re.sub('[^a-zA-Z0-9]',' ', str(text))
    review = review.lower()
    review = review.split()
    review = [word for word in review if word not in stopwords.words ('english')]
    review = ' '.join(review)
    return review


# In[7]:


#opening the file of positive and negative words in google drive

posfile = open("C:\IIT BSc. Data Science and Programming\Internships\positive-words.txt",'r')
negfile = open("C:\\IIT BSc. Data Science and Programming\\Internships\\negative-words.txt",'r')


# In[8]:


#reading the files containing positive, negative words

pos = posfile.readlines()
neg = negfile.readlines()


# In[9]:


#obtaining the positive and negative words in desired format (2 separate lists, words separated by comma, removing unnecessary spaces)

pos_list = []
for i in pos:
    pos_list.append(i.replace('\n',''))
    
neg_list = []
for i in neg:
    neg_list.append(i.replace('\n',''))


# In[10]:


print(pos_list[:5])


# In[11]:


print(neg_list[:5])


# In[12]:


#function for obtaining positive score (+1 is assigned to all the  words, their frequencies are calculated)

def pos_score(trans):
    pos_score = 0
    st = trans
    dic_pos = {} #creates an empty dictionary
    count = 0
    for i in st.split(' '):
        if i in dic_pos and i in pos_list:            #forming a dictionary containing frequencies of positive words
            dic_pos[i] = dic_pos[i]+1
        elif i not in dic_pos and i in pos_list:
            dic_pos[i] = 1
    for i in dic_pos:
        pos_score = pos_score + dic_pos[i]           #positive score = 1* frequency of positive words occuring
    return pos_score


# In[13]:


#function  for obtaining negative score (-1 is assigned to all the words, their frequencies are calculated)

def neg_score(trans):
    neg_score = 0
    st = trans
    dic_neg = {} #creates an empty dictionary
    count = 0
    for i in st.split(' '):
        if i in dic_neg and i in neg_list:            #forming a dctionary containing frequencies of negative words
            dic_neg[i] = dic_neg[i]+1
        elif i not in dic_neg and i in neg_list:
            dic_neg[i] = 1
    for i in dic_neg:
        neg_score = neg_score + dic_neg[i]            #negative score is -(-1)* frequncy of negative words
    return neg_score


# In[14]:


#function for calculating average sentence length

def av_sen_length(set_up):
    con = ''
    for i in set_up:
        for j in i:
            con = con+' '+j
    con = con.strip()
    from nltk import tokenize
    p = con

    sen = tokenize.sent_tokenize(p)      #the article is tokenized first to obtaining a list separated by different sentences
    
    #sentence count
    sencount = 0
    for i in sen:
        sencount = sencount + 1
        
    #words count
    wordcount=0
    for  i in set_up:  
            for j in i:
                wordcount = wordcount + 1
                
    #average sentence length
    av_sen_len = wordcount/sencount
    
    return av_sen_len


# In[15]:


#module for tokenizing on the basis of syllables

from nltk.tokenize.sonority_sequencing import SyllableTokenizer


# In[16]:


#defining a function to obtain complex words (syllables more than 2)

def hardword():
    words = ''
    hardwordlist = []
    l = []

        # Create a reference variable for Class word_tokenize to split the word on the basis of syllables
    tk = SyllableTokenizer()                        

        # Create a string input
    syllable = []
    for i in trans.split(' '):
        for j in i.split(' '):
            if j.isalpha():                   #syllable is a list which stores the words as separate lists split by the syllable
                syllable.append(tk.tokenize(j)) 
    syllable            
    for i in syllable:
        if len(i)>2:                          #retaining only the syllables which have more than 2 syllables
            l.append(i)
    for i in l:
        hardwordlist.append(''.join(i))
    return hardwordlist


# In[17]:


#words count original text
def count(set_up):
    wordcount=0
    for  i in set_up:  
            for j in i:
                wordcount = wordcount + 1
    return wordcount            


# In[18]:


def syllablecountperword(trans):
    tk = SyllableTokenizer()

        # Create a string input
    syllable = []
    for i in trans.split(' '):
        for j in i.split(' '):
            if j.isalpha():                   #syllable is a list which stores the words as separate lists split by the syllable
                syllable.append(tk.tokenize(j))  
                
    syllablelen = 0
    for i in syllable:
        syllablelen = syllablelen + len(i)     #total number of syllables present in overall text/number of words (analysis done after cleaning text)
    syllable_length = syllablelen/len(syllable)
    return syllable_length


# In[19]:


def averagewordlength(set_up):
    wordsnum = count(set_up)
    length = 0
    for i in set_up:
        for j in i:
            length = length+len(j)
    return length/wordsnum


# In[20]:


#defining function to calculate number of pronouns

def pronouns(set_up):
    para=''
    for i in set_up:
        for j in i:
            para = para+' '+j
            
    para = para.strip().split(' ')     #obtaining a list of words in the article
    
    import re

    i = re.findall("I", str(para))
    we = re.findall("we", str(para))   #using re module we find if prounouns are present (considering upper and lower cases)
    We = re.findall("We", str(para))
    ours = re.findall("ours", str(para))
    Ours = re.findall("Ours", str(para))
    us = re.findall("us", str(para))
    lengths = len(i) + len(we) + len(We) + len(ours) + len(Ours) + len(us)
    return lengths


# In[21]:


#overall code
for num in range(1,151):
    answer = []
    required = []
    df = open(f'C:\\Users\\Administrator\\{num}.txt','r', encoding = 'utf-8')
    txt = df.readlines()
    set_up = setup(txt)
    trans = transform(set_up)
    positive_score = pos_score(trans)      #calculates +ve score
    negative_score = neg_score(trans)      #calculates -ve score
    polarity_score = (positive_score - negative_score)/((positive_score + negative_score) + 0.000001)    #calculates polarity
    subjectivity_score = (positive_score + negative_score)/ ((len(trans.split(' '))) + 0.000001)     #calculates subjectivity
    average_sentence_length = av_sen_length(set_up)      #calculates average sentence length
    hardwordnumber = len(hardword())                     #calculates number of complex words
    percent_complex = hardwordnumber/count(set_up)       #calculates % of complex words
    fog_index = 0.4 * (average_sentence_length + percent_complex)      #calculates fog index
    average_number_of_words_per_sentence = av_sen_length(set_up)       #caculates average number of words per sentence
    complex_word_count = hardwordnumber                            #calulates number of complex words
    word_count = len(trans.split(' '))                              #calculates number of words in text after cleaning
    syllableperword = syllablecountperword(trans)                  #calultes numner of syllables per word
    pronouns_num = pronouns(set_up)
    avwordlength = averagewordlength(set_up)
    answer.append([positive_score, negative_score, polarity_score, subjectivity_score, average_sentence_length, percent_complex, fog_index,average_number_of_words_per_sentence, complex_word_count, word_count, syllableperword, pronouns_num, avwordlength])
    for i in answer:
        li = i
   
    #appending the variables calculated in the dataframe
    
    answer_df['POSITIVE SCORE'][num-1] = round(li[0], 2)
    answer_df['NEGATIVE SCORE'][[num-1]] = round(li[1], 2)
    answer_df['POLARITY SCORE'][num-1] = round(li[2], 2)
    answer_df['SUBJECTIVITY SCORE'][num-1] = round(li[3], 2)
    answer_df['AVG SENTENCE LENGTH'][num-1] = round(li[4], 2)
    answer_df['PERCENTAGE OF COMPLEX WORDS'][num-1] = round(li[5], 2)
    answer_df['FOG INDEX'][num-1] = round(li[6], 2)
    answer_df['AVG NUMBER OF WORDS PER SENTENCE'][num-1] = round(li[7],2)
    answer_df['COMPLEX WORD COUNT'][num-1] = round(li[8], 2)
    answer_df['WORD COUNT'][num-1] = round(li[9], 2)
    answer_df['SYLLABLE PER WORD'][num-1] = round(li[10], 2)
    answer_df['PERSONAL PRONOUNS'][num-1] = round(li[11], 2)
    answer_df['AVG WORD LENGTH'][num-1] = round(li[12], 2)
    #print(trans)
    print(num,"done")      #keeps a check on what file is being executed


# In[22]:


answer_df      #final output table


# In[23]:


#saving the output table

answer_df.to_csv(r"C:\IIT BSc. Data Science and Programming\Internships\Final_Ouput.csv", index=False)


# In[ ]:




