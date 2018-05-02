
# coding: utf-8

# In[24]:


# -*- coding: utf-8 -*-
import csv
import pandas
import glob
import os
import sys
from textblob import TextBlob
import nltk
from langdetect import detect
from operator import itemgetter
from statistics import mean
import six
#reload(sys)
#sys.setdefaultencoding('utf8')




# In[6]:


rootPath='Accounts/q1_output/*.csv'
rootResultPath='Accounts/q2_output/'


files = glob.glob(rootPath)
#files_comments = glob.glob(rootPath_comments)

names = [os.path.basename(x) for x in glob.glob(rootPath)]

files


# In[25]:


OUTPUT_COLS = ['id','date_published','link','caption_original',
               'caption_cleaned','hashtags','num_comments','num_shares',
               'num_likes','Reactions_SUM','category','matched_keywords',
               'language','average_sentiment_score','sentiment']



#Merge all DATA
merged = pandas.DataFrame(columns=OUTPUT_COLS)



# In[5]:


for file, name in zip(files, names):
    info=pandas.read_csv(file)
    merged=merged.append(info)
    info['date_published']=pandas.to_datetime(info['date_published'])

    period=info['date_published'].dt.to_period('M')


    months = info.groupby([period])


    for month, group in months:
        group.sort_values(by=['Reactions_SUM'],ascending=False).to_csv(rootResultPath+str(month)+'-'+name,index=None)


# In[10]:


merged[OUTPUT_COLS+['account_name']].to_csv(rootResultPath+'merged_ALL.csv', encoding='utf-8', index=None)

#########################################################



# In[26]:


info=pandas.read_csv('Accounts/q2_output/merged_ALL.csv', encoding='utf-8')
info['date_published']=pandas.to_datetime(info['date_published'])
period=info['date_published'].dt.to_period('M')
months = info.groupby([period])

months


# In[27]:


for month, group in months:
    group.sort_values(by=['Reactions_SUM'],ascending=False).to_csv(rootResultPath+str(month)+'.csv', encoding='utf-8', index=None)

    
##########################################################


# In[33]:


rootPath='Accounts/q2_output/months/*.csv'

files = glob.glob(rootPath)
#files_comments = glob.glob(rootPath_comments)
names = [os.path.basename(x) for x in glob.glob(rootPath)]  
merged = pandas.DataFrame(columns=OUTPUT_COLS)
files


# In[37]:


for file, name in zip(files, names):
    info=pandas.read_csv(file, encoding='utf-8')

    merged=merged.append(info.head(3))

print(merged.columns)
print(OUTPUT_COLS)


# In[39]:


merged[OUTPUT_COLS+['account_name']].to_csv(rootResultPath+'merged_TOP3_monthly.csv', index=None)

