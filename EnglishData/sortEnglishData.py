
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


outputDir = os.path.dirname(data_folder) + '/output/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


# In[4]:


stopWords = set(stopwords.words('english'))
stopWords.add('theyre')
exclude = set(string.punctuation)

lemma = WordNetLemmatizer()


def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang


def lemmatize_keywords(col):
    if str(col).lower() == 'nan':
        return ''
    return '_'.join(lemma.lemmatize(word).lower() for word in col.split()) 


def lemmatize_text(row):    
    text_cols = str(row['caption_cleaned']).lower(), str(row['hashtags']).lower()
    lemmatized_text = []
    if text_cols[0] == 'nan':
        return '', ''
    for text in text_cols:
        if isinstance(text, str):
            #print(text)
            text = text.replace('’', '\'')
            #print(text)
            tokens = tokenizer.tokenize(text.split())            
            stop_free = ' '.join(w for w in tokens if w not in stopWords and len(w) > 1)
            punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
            lemmas = ' '.join(lemma.lemmatize(word).lower() for word in punc_free.split() if len(lemma.lemmatize(word)) > 2)
            stop_free_2 = ' '.join(w for w in lemmas.split() if w not in stopWords and len(w) > 1)
            #print(stop_free_2)
            lemmatized_text.append(stop_free_2.split())
        else:
            lemmatized_text = ['', '']
    return lemmatized_text[0], lemmatized_text[1]


def find_category(row):
    text_cols = row['lemmatized_caption_cleaned'], row['lemmatized_hashtags']
    keywords_found = []
    counter = {'Social': 0, 'Economical': 0, 'Environmental': 0}
    category = 'unknown'
    for text in text_cols:
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


# In[5]:


# load keywords list
pd.options.display.max_rows = 10
KEYWORD_COL = ['Social', 'Economical', 'Environmental']
keywords_df = pd.read_csv(keywords_chosen, encoding='utf-8')   # "ISO-8859-1"
lemma_keywords_df = pd.DataFrame(columns=KEYWORD_COL)
for col in KEYWORD_COL:
    lemma_keywords_df[col] = keywords_df[col].astype(str).apply(lemmatize_keywords)

soc_list = set(lemma_keywords_df['Social'].tolist())
econ_list = set(lemma_keywords_df['Economical'].tolist())
env_list = set(lemma_keywords_df['Environmental'].tolist())
keywords_list = soc_list.union(econ_list).union(env_list)

punc_keep = set()
for word in keywords_list:
    for char in word:
        if char in exclude:
            punc_keep.add(char)

for punc in punc_keep:
    exclude.remove(punc)

multi_word = [w.split('_') for w in keywords_list ]   #if '_' in w 
tokenizer = MWETokenizer(multi_word)


# In[6]:


pd.options.display.max_rows = 100
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)  
for filename in filePaths:
    print(filename)
    basename = os.path.basename(filename)
    outputFileName = outputDir + basename
    #print(outputFileName)
    data_df = pd.read_csv(filename, encoding = 'utf-8')
    data_df['lang'] = data_df['caption_cleaned'].astype(str).apply(detect_lang)
    wrong_lang = data_df[data_df['lang'] != 'en'].shape[0]    
    print(wrong_lang/len(data_df))
    data_df['lemmatized_caption_cleaned'], data_df['lemmatized_hashtags']  = zip(*data_df.apply(lemmatize_text, axis=1))
    data_df['matched_keywords'], data_df['category'] = zip(*data_df.apply(find_category, axis=1))
    
    #display(data_df[['words_matched_list', 'lemmatized_caption_cleaned','matched_keywords', 'category']])
    del data_df['words_matched_list']
    del data_df['lang']
    del data_df['lemmatized_caption_cleaned']
    del data_df['lemmatized_hashtags']
    output_list = ['Unnamed: 0', 'id', 'date_published', 'link', 'caption_original',
       'caption_cleaned', 'hashtags', 'num_shares', 'num_likes',
       'Reactions_SUM', 'category', 'language', 'average_sentiment_score',
       'sentiment', 'account_name', 'matched_keywords', 'category']
    output_df = data_df[output_list]
    output_df.to_csv(outputFileName, index=None)    


# In[7]:


#print(stopWords)

