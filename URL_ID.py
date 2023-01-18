#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup,NavigableString
data = pd.read_excel('Input.xlsx')
data.head()
data.tail()


# In[2]:


#to create a folder for all the files
import os

if not os.path.exists('data'):
    os.makedirs('data')


# In[56]:


l=[]
for url in data['URL']:
    title=url.split('/')[3]
    file_name=title+'.html'
    file_path='./data/' + file_name 
    #to scrape the data from the url and save it to the file if the file doesnt exist in the directory
    if not os.path.exists(file_path):
        #print('file doesnt exists')
        r = requests.get(url, headers={"User-Agent": "XY"})
        r.encoding = 'utf-8'
        htmlcontent=r.text
        with open(file_path,'w', encoding='utf-8') as f:
            f.write(htmlcontent)
    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            htmlcontent = f.read()
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    title = soup.title
    article_content = soup.find('div', attrs={'class': 'td-post-content'})
    if article_content is None:
        #print('break')
        continue
    article_text=''
    for element in article_content:
        if not isinstance(element, NavigableString):
            text = element.text
            article_text+=text
    l.append(article_text)

df=pd.DataFrame(l,columns=['Text'])
df.head()


# In[49]:


df.shape


# In[16]:


import pandas as pd
outputfile=pd.read_excel('Output Data Structure.xlsx')
outputfile.head()


# In[57]:


#from nltk.tokenize import word_tokenize


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
l=[]
for i in range(len(df)):
    
    example_sent = df['Text'][i]
  
    stop_words = set(stopwords.words('english'))
  
    word_tokens = word_tokenize(example_sent)
  
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
  
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    
    new_sentence=' '.join(filtered_sentence)
    l.append(new_sentence)
df=pd.DataFrame(l,columns=['Text'])
  
#print(word_tokens)
df.head()


# In[59]:


#to read the Positive-scores.txt file as a dataframe and changing the first entry


import pandas as pd
pw=pd.read_csv('positive-words.txt')

new_row=pd.DataFrame({'a+':'a+'},index=[0])
pw=pd.concat([new_row,pw.loc[:].reset_index(drop=True)])
pw.columns=['0']
pw.reset_index(drop=True,inplace=True)
pw.head(100)


# In[24]:


# code to find and enter the the positive score of each url file in the output file

for i in range(len(df)):
    ps=0
    #print(type(df['Text'][i]))
    for word in pw['0']:
        
        if word in df['Text'][i].lower():
            ps+=1
    outputfile.at[i,'POSITIVE SCORE']=ps

outputfile.head()  


# In[26]:


#code to read and change the negative_words file data to a dataframe
with open('negative-words.txt', 'rb') as nw:
    words = [str(w)[2:-3]for w in nw]
    
    nw=pd.DataFrame(words,columns=['Negative_words'])
    
    print(nw)


# In[27]:


#code to find the negative score of each url file in the output file
for i in range(len(df)):
    ns=0
    #print(type(df['Text'][i]))
    for word in nw['Negative_words']:
        
        if word in df['Text'][i].lower():
            ns+=1
    outputfile.at[i,'NEGATIVE SCORE']=ns

outputfile.head() 


# In[69]:


#polarity_score=(pos-nes)/((pos+nes)+0.000001)
for i in range(len(outputfile)):
    pols=0
    pos=outputfile['POSITIVE SCORE'][i]
    nes=outputfile['NEGATIVE SCORE'][i]
    pols=(pos-nes)/((pos+nes)+0.000001)
        
        
    outputfile.at[i,'POLARITY SCORE']=pols

outputfile.head()


# In[70]:


#SUBJECTIVITY SCORE=(pos+nes)/((total no.of words)+0.000001)
for i in range(len(df)):
    
    #print(type(df['Text'][i]))
    text=df['Text'][i].split()
    pos=outputfile['POSITIVE SCORE'][i]
    nes=outputfile['NEGATIVE SCORE'][i]
    nofwords=len(text)
    subs=(pos+nes)/(nofwords+0.000001)
        
        
    outputfile.at[i,'SUBJECTIVITY SCORE']=subs

outputfile.head() 


# In[71]:


#avg sentence length= the number of words / the number of sentences
from nltk.tokenize import sent_tokenize,word_tokenize
for i in range(len(df)):
    
    #print(type(df['Text'][i]))
    text=df['Text'][i]
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    nofwords=len(word_list)
    nofsents=len(sent_tokenize(text))
    avgsl=(nofwords)/(nofsents+0.000001)
        
        
    outputfile.at[i,'AVG SENTENCE LENGTH']=avgsl

outputfile.head()


# In[72]:


#POCW=nofcw/nofwords
pofcw=0
for i in range(len(df)):
    text=df['Text'][i]
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    nofwords=len(word_list)
    vowels='aeiou'
    nofcw=0
    for w in word_list:
        vc=0 #vowelcount
        for v in vowels:
            if v in w:
                vc+=1
        if vc>1:
            nofcw+=1
                
    pofcw=nofcw/nofwords
    
    outputfile.at[i,'PERCENTAGE OF COMPLEX WORDS']=pofcw
    
outputfile.head()


# In[73]:


#fogi=0.4*(avgsl+pofcw)
fogi=0
for i in range(len(df)):
    text=df['Text'][i]
    
    #to find avgsl
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    nofwords=len(word_list)
    nofsents=len(sent_tokenize(text))
    avgsl=(nofwords)/(nofsents+0.000001)
    
    #to find pofcw
    vowels='aeiou'
    nofcw=0
    for w in word_list:
        vc=0 #vowelcount
        for v in vowels:
            if v in w:
                vc+=1
        if vc>1:
            nofcw+=1
    pofcw=nofcw/nofwords
    
    fogi=0.4*(avgsl+pofcw)
    
    outputfile.at[i,'FOG INDEX']=fogi

outputfile.head()  


# In[74]:


#anofwps=nofwords/nofsents
for i in range(len(df)):
    text=df['Text'][i]
    
    #to find avgsl
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    nofwords=len(word_list)
    nofsents=len(sent_tokenize(text))
    anofwps=nofwords/nofsents
    
    outputfile.at[i,'AVG NUMBER OF WORDS PER SENTENCE']=anofwps

outputfile.head()  


# In[75]:


for i in range(len(df)):
    text=df['Text'][i]
    
    vowels='aeiou'
    nofcw=0
    
    for w in word_list:
        for v in vowels:
            if v in w:
                nofcw+=1
                break
    
    
    outputfile.at[i,'COMPLEX WORD COUNT']=nofcw
    
outputfile.head()


# In[76]:


#remove the stop words
#remove the punctuations
for i in range(len(df)):
    text=df['Text'][i]

    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    nofwords=len(word_list)
    outputfile.at[i,'WORD COUNT']=nofwords
outputfile.head()


# In[77]:


#scpw=total no. of syllables in the text/total no of words
for i in range(len(df)):
    text=df['Text'][i]
    vowels='aeiou'
    nofs=0
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    
    nofwords=len(word_list)
    for l in text:
        if l in vowels:
            nofs+=1
    
    scpw=nofs/nofwords  
    
    
    
    outputfile.at[i,'SYLLABLE PER WORD']=nofs
    
outputfile.head()


# In[78]:


ppc=0
pp=['I','we','We','WE','my','My','MY','ours','OURS','Ours','us','Us']
for i in range(len(df)):
    ppc=0
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    for w in word_list:
        if w in pp:
            ppc+=1
    outputfile.at[i,'PERSONAL PRONOUNS']=ppc
outputfile.head()


# In[79]:


#avgwl=sum of the no of chars in each word/total no ofwords
for i in range(len(df)):
    text=df['Text'][i]
    #to find no. of words
    clean_text = ''.join((c for c in text if c.isalpha() or c.isspace()))
    word_list = word_tokenize(clean_text)
    nofwords=len(word_list)
    
    #to find sum of chars
    nofc=0
    for w in word_list:
        cpw=len(w)
        nofc+=cpw
    avgwl=nofc/nofwords
        
    
    outputfile.at[i,'AVG WORD LENGTH']=avgwl
outputfile.head()


# In[80]:


outputfile.to_csv('outputfile.csv',index=False)


# In[81]:


df = pd.read_csv('outputfile.csv')
df

