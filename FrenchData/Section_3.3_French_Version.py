
# coding: utf-8

# In[1]:


import glob
import os
import sys
import pandas as pd

import nltk
#nltk.download()   # comment after first download
from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
from FrenchLefffLemmatizer.FrenchLefffLemmatizer import FrenchLefffLemmatizer
import string
from numbers import Number
from pprint import pprint
import logging
import operator

pd.options.display.max_rows = 30


# In[2]:


fr_file = './Accounts/q3q4_output/*.csv'

keywords_chosen = '13_FSDS_Goals_Keywords_FR.csv'

OUTPUT_COLS = ['id', 'num_comments', 'num_shares',
               'num_angrys', 'num_hahas', 'num_likes', 'num_loves', 'num_sads',
                'num_special', 'num_wows', 'Reactions_SUM', 
               'FSDS_matched_keywords', 'FSDS_category']


# In[3]:


# read csv files and save targt columns to dataframe
# all files in q3q4output get merged into one df
filePaths = glob.glob(fr_file)
data_df = pd.DataFrame(columns=OUTPUT_COLS)
for filename in filePaths:
    #print(filename)    
    df_i = pd.read_csv(filename, encoding = 'utf-8')
    data_df = data_df.append(df_i, ignore_index=True)

data_df = data_df[OUTPUT_COLS]
data_df


# In[4]:


# set of punctuations to remove from text
exclude = set(string.punctuation)

stopWords = set(stopwords.words('french'))

lemma = FrenchLefffLemmatizer()    # French lemmatizer


# lemmatize_keywords also clears 'nan' from input keyword list file
# lemmatization is conducted based on context, some words may not get lemmatized, 
# e.g. "local eating" does not get lemmatized to "local eat"
def lemmatize_keywords(col):
    if str(col).lower() == 'nan':
        return ''
    return '_'.join(lemma.lemmatize(word).lower() for word in col.replace('’', '\'').replace('.', '').split()) #


# In[5]:


# load keywords list
pd.options.display.max_rows = 100
keywords_df = pd.read_csv(keywords_chosen, encoding='utf-8')   # "ISO-8859-1"
KEYWORDS_COLS = keywords_df.columns
lemma_keywords_df = pd.DataFrame(columns=KEYWORDS_COLS)
category_dict = {}
keywords_list = set()
for col in KEYWORDS_COLS:
    lemma_keywords_df[col] = keywords_df[col].astype(str).apply(lemmatize_keywords)
    category_dict[col.lower()] = set(lemma_keywords_df[col].tolist())
    #category_dict[col.lower()].remove('')
    keywords_list = keywords_list.union(category_dict[col.lower()])


# In[6]:


data_df['FSDS_category'] = data_df['FSDS_category'].str.lower()


# In[7]:


data_df['FSDS_category'] = data_df['FSDS_category'].str.replace('unknown', 'other')
#data_df['FSDS_category'] = data_df['FSDS_category'].str.replace('connecting canadians with nature ', 'connecting canadians with nature')


# In[8]:


output_df = data_df.groupby(['FSDS_category']).sum().reset_index()
output_df#.columns = ['FSDS_category', 'sentiment', 'senti_count']


# In[9]:


def find_topics(row):
    matched_words = row['FSDS_matched_keywords'].replace('\', \'', ',').replace('\'][\'', ',').replace('[\'', '').replace('\']', '').replace('[]', '')
    if matched_words == '':
        return ''
    print('Processing FSDS Goal: ' + row['FSDS_category'])
    matched_word_list = matched_words.split(',')
    matched_word_set = set(matched_word_list)
    remove_words = []
    for word in matched_word_set:
        if word not in category_dict[row['FSDS_category']]:
            remove_words.append(word)
            #print('This word does not belong to this category: ' + word)
    for word in remove_words:
        matched_word_set.remove(word)
    counter = {}
    for word in matched_word_set:
        counter[word] = 0
    #print(counter)
    for word in matched_word_list:
        if word in category_dict[row['FSDS_category']]:
            counter[word] += 1
    print(counter)
    result = sorted(counter, key=counter.get, reverse=True)
    
    return str(', '.join(result[0:8]))


# In[10]:


output_df.columns
output_df['Topics/Issues'] = output_df.apply(find_topics, axis=1)


# In[11]:


REACTION_COLS = ['num_comments', 'num_shares', 'num_angrys', 'num_hahas', 'num_likes', 'num_loves', 'num_sads',
                'num_special', 'num_wows',]
def merge_reaction(row):
    merge = ''
    for col in REACTION_COLS:
        merge += col[4:] + ': ' + str(row[col]) + '\n'
    merge += 'Reactions SUM: ' + str(row["Reactions_SUM"])
    return merge
    


# In[12]:


output_df['Reaction summary'] = output_df.apply(merge_reaction, axis=1)
output_df = output_df[['FSDS_category', 'Reaction summary', 'Topics/Issues']]
output_df.columns = ['FSDS Goal', 'Reaction Summary', 'Topics/Issues']
output_df['FSDS Goal'] = output_df['FSDS Goal'].str.title()
output_df


# In[15]:


output_df['Reaction Summary']


# In[14]:


output_df.to_csv('./section3-3_table_fr.csv', index=None)

