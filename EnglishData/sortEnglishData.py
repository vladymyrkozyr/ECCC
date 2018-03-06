
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd

from langdetect import detect
import nltk
#nltk.download()   # comment after first download
from nltk.tokenize import wordpunct_tokenize, MWETokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import gensim
from gensim import corpora
import string
from numbers import Number
from pprint import pprint
import logging
import operator

pd.options.display.max_rows = 30


# In[2]:


keywords_chosen = 'Keywords_ECCC_EN.csv'

data_folder = './Accounts/*.csv'

CSV_COLUMNS = ['caption_cleaned', 'hashtags']


# In[3]:


# create output directory
outputDir = os.path.dirname(data_folder) + '/output/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


# In[4]:


# set of punctuations to remove from text
exclude = set(string.punctuation)


# In[5]:


stopWords = set(stopwords.words('english'))
stopWords.add('theyre')   # an informal spelling

lemma = WordNetLemmatizer()    # NLTK English lemmatizer

# detect_lang function can be use to check the percentage of non English posts
# note that missing value NaN can be detected as many different languages such english, spanish or italian
def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang

# lemmatize_keywords also clears 'nan' from input keyword list file
# lemmatization is conducted based on context, some words may not get lemmatized, 
# e.g. "local eating" does not get lemmatized to "local eat"
def lemmatize_keywords(col):
    if str(col).lower() == 'nan':
        return ''
    return '_'.join(lemma.lemmatize(word).lower() for word in col.split()) 


# In[6]:


# load keywords list
pd.options.display.max_rows = 10
KEYWORD_COL = ['Social', 'Economical', 'Environmental']
keywords_df = pd.read_csv(keywords_chosen, encoding='utf-8')   # "ISO-8859-1"
lemma_keywords_df = pd.DataFrame(columns=KEYWORD_COL)
for col in KEYWORD_COL:
    lemma_keywords_df[col] = keywords_df[col].astype(str).apply(lemmatize_keywords)
#display(lemma_keywords_df)
soc_list = set(lemma_keywords_df['Social'].tolist())
econ_list = set(lemma_keywords_df['Economical'].tolist())
env_list = set(lemma_keywords_df['Environmental'].tolist())
keywords_list = soc_list.union(econ_list).union(env_list)

# if there are punctuations in the keywords list, these punctuation will be kept regardless of puncturation removal step
punc_keep = set()
for word in keywords_list:
    for char in word:
        if char in exclude:
            punc_keep.add(char)

for punc in punc_keep:
    exclude.remove(punc)

# Add all words in the given keyword list to pre-defined token dictionary
multi_word = [w.split('_') for w in keywords_list ]   #if '_' in w 
tokenizer = MWETokenizer(multi_word)


# In[7]:


def lemmatize_text(row): 
    #print(row['Unnamed: 0'])
    caption_cleaned =  str(row['caption_cleaned']).replace('nan', '')
    # because the "hashtags" column is a string but not a list anymore, the following removes [,]
    hashtags = str(row['hashtags'])
    hashtags = hashtags.replace('[', '')
    hashtags = hashtags.replace(']', '')
    hashtags = hashtags.replace('\'', '')
    hashtags = hashtags.replace(',', '')
    # keyword search is done on both cleaned caption and hashtags
    text = hashtags + ' '+ caption_cleaned
    #print(text)
    text = text.replace('’', '\'')
    tokens = tokenizer.tokenize(text.split())   
    # remove stop words
    stop_free = ' '.join(w for w in tokens if w not in stopWords and len(w) > 1)
    # remove punctuation
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    # lemmatize
    lemmas = ' '.join(lemma.lemmatize(word).lower() for word in punc_free.split() if len(lemma.lemmatize(word)) > 2)
    # remove stop words that appear after lemmatization
    stop_free_2 = ' '.join(w for w in lemmas.split() if w not in stopWords and len(w) > 1)
    #print(stop_free_2)
    return stop_free_2.split()

# assign a category based the max number of keywords found in each category
def find_category(row):
    text = row['lemmatized_text']
    keywords_found = []
    counter = {'Social': 0, 'Economical': 0, 'Environmental': 0}
    category = 'unknown'
    for word in text:
        if word in soc_list:
            counter['Social'] += 1
            keywords_found.append(word)
        if word in econ_list:
            counter['Economical'] += 1
            keywords_found.append(word)
        if word in env_list:
            counter['Environmental'] += 1
            keywords_found.append(word)
    if len(keywords_found) > 0:
        category = max(counter.items(), key=operator.itemgetter(1))[0]    
    return keywords_found, category


# In[8]:


pd.options.display.max_rows = 100
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)  
for filename in filePaths:
    print(filename)
    basename = os.path.basename(filename)
    outputFileName = outputDir + basename
    data_df = pd.read_csv(filename, encoding = 'utf-8')
    if data_df.shape[0] < 1:
        data_df.to_csv(outputFileName, index=None) 
        continue
    #data_df['lang'] = data_df['caption_cleaned'].astype(str).apply(detect_lang)
    data_df = data_df.drop(['category','words_matched_list'], axis=1)
    #wrong_lang = data_df[data_df['lang'] != 'en'].shape[0]
    data_df['lemmatized_text'] = data_df.apply(lemmatize_text, axis=1)
    data_df['matched_keywords'], data_df['category'] = zip(*data_df.apply(find_category, axis=1))
    
    #display(data_df[['words_matched_list', 'lemmatized_text','matched_keywords', 'category']])
    output_list = data_df.columns.tolist()
    #output_list.remove('lang')
    output_list.remove('lemmatized_text')
    output_list.append('category')
    output_df = data_df[output_list]
    output_df.to_csv(outputFileName, index=None)    
