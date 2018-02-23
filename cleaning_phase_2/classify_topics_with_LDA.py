
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd
from langdetect import detect
import nltk
#nltk.download()   # comment after first download
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import gensim
from gensim import corpora
import string
from pprint import pprint
import logging

pd.options.display.max_rows = 20


# In[2]:


# set number of topics to classify
NUM_TOPICS = 3


# In[3]:


# list = [social_media_csv_filepath, cleaned_text_column_name, raw_text_column_name]
tw_list = ['../tw/filtered_data_spell_corrected/*.csv', 'full_text_cleaned', 'text_original']
fb_list = ['../fb/filtered_data_spell_corrected/statuses/*.csv', 'status_message_cleaned', 'text_original']
in_list = ['../in/filtered_data_spell_corrected/posts/*.csv', 'caption', 'text_original']


# In[4]:


stopWords_en = set(stopwords.words('english'))
stopWords_fr = set(stopwords.words('french'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()


# read csv files and save targt columns to dataframe
def import_csv_columns(list_loc):
    filePaths = glob.glob(list_loc[0])  
    df_loc = pd.DataFrame(columns=['cleaned_text', 'raw_text'])
    for filename in filePaths:
        #print(os.path.basename(filename))
        df_raw = pd.read_csv(filename)
        df_two_col = df_raw[[list_loc[1], list_loc[2]]]
        df_two_col.columns = df_loc.columns
        #display(len(df_two_col))
        df_loc = df_loc.append(df_two_col, ignore_index=True)
        #display(len(df_merge))
    df_loc = df_loc.dropna(axis=0, how='any')
    #print(len(df_loc))
    return df_loc


def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang


def normalize_text(row):   
    text = row['cleaned_text']
    stopWords = stopWords_en  
    if row['lang'] == 'fr':
        stopWords = stopWords_fr  
    stop_free = ' '.join([w for w in wordpunct_tokenize(text) if w.lower() not in stopWords
            and len(w) > 1 and w.isalnum()]) 
    punc_free = ''.join(ch.lower() for ch in stop_free if ch not in exclude)
    normalized = ' '.join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized.split()


# In[ ]:


# combine Twitter's tweets, Facebook's posts & Instagram's captions into dataframe 'df_merge'.
df_merge = pd.DataFrame(columns=['cleaned_text', 'raw_text'])
df_merge = df_merge.append(import_csv_columns(tw_list), ignore_index=True)
df_merge = df_merge.append(import_csv_columns(fb_list), ignore_index=True)
df_merge = df_merge.append(import_csv_columns(in_list), ignore_index=True)
df_merge


# In[ ]:


# Detect language of a post. Several languages other than english or french are dectecd but makes up less than 1%
df_merge['lang'] = df_merge['cleaned_text'].apply(detect_lang)
df_merge.groupby('lang').count()


# In[ ]:


# filter out exotic languages
df_merge = df_merge[(df_merge['lang'] == 'en') | (df_merge['lang'] == 'fr')]


# In[ ]:


# pre-processing text for LDA
df_merge['normalized_text'] = df_merge.apply(normalize_text, axis=1)
df_merge['normalized_text']


# In[ ]:


# train two LDA models, one for 'English', the other for 'French'
for lang in ['en', 'fr']:
    df_sub = df_merge[df_merge['lang'] == lang]
    doc_clean = df_sub['normalized_text'].tolist() 
    
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    dictionary.save('LDA_dictionary_' + lang + '.dict')  # store the dictionary, for future reference
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    corpus = [dictionary.doc2bow(doc) for doc in doc_clean]
    corpora.MmCorpus.serialize('LDA_corpus_' + lang + '.mm', corpus)
    pprint(len(dictionary.token2id))
    
    logging.basicConfig(filename='lda_model_' + lang + '.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    print('training model for ' + lang)
    # Running and Training LDA model on the document term matrix.
    ldamodel = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=5)
    
    # save results
    result = ldamodel.show_topics(num_topics=NUM_TOPICS, num_words=100, formatted=False)
    df_concat = pd.DataFrame()
    for i in range(0, NUM_TOPICS):
        df_tmp = pd.DataFrame(result[i][1], columns=['#' + str(result[i][0]) + '_word', '#' + str(result[i][0]) + '_prob'])
        df_concat = pd.concat([df_concat, df_tmp], axis=1)
        #display(df_concat)
    df_concat.to_csv('../LDA_classify_topics_' + lang + '.csv', index=None) 


# In[ ]:


## Experiment on LSI model

# extract 3 LSI topics; use the default one-pass algorithm
lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=dictionary, num_topics=NUM_TOPICS)
# print the most contributing words (both positively and negatively) for each of the first ten topics
lsi.print_topics()

