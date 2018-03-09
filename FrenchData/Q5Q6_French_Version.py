
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd
import nltk
#nltk.download()   # comment after first download
from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
from FrenchLefffLemmatizer.FrenchLefffLemmatizer import FrenchLefffLemmatizer
import gensim
from gensim import corpora
from gensim.models import Word2Vec
import string
from numbers import Number
from pprint import pprint
import logging
import operator
from pprint import pprint
pd.options.display.max_rows = 30


# In[2]:


keywords_chosen = 'Que5_Que6_FR_KeywordLists.csv'

data_folder = './Accounts/*.csv'
OUTPUT_COLS = ['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments',
               'num_shares','num_likes','Reactions_SUM','category','matched_keywords','language',
               'average_sentiment_score','sentiment', 'Action_matched_keywords']


# create output directory
outputDir = os.path.dirname(data_folder) + '/q5q6_output/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


# set of punctuations to remove from text
exclude = set(string.punctuation)


stopWords = set(stopwords.words('french'))
lemma = FrenchLefffLemmatizer()


# lemmatize_keywords also clears 'nan' from input keyword list file
# lemmatization is conducted based on context, some words may not get lemmatized, 
# e.g. "local eating" does not get lemmatized to "local eat"
def lemmatize_keywords(col):
    if col.lower() == 'nan':
        return ''
    # if a stopword appreas in given keyword list, this stopword will be removed from stopword list
    for keyword in col.split():
        if keyword in stopWords:
            print(keyword)
            stopWords.remove(keyword)
    return '_'.join(lemma.lemmatize(word).lower() for word in col.replace('’', '\'').replace('.', '').split()) #lemma.lemmatize(word)




# load keywords list
pd.options.display.max_rows = 100
keywords_df = pd.read_csv(keywords_chosen, encoding='utf-8')

keywords_df['lemmatized_keywords'] = keywords_df['Actions to advance sustainablity'].astype(str).apply(lemmatize_keywords)
keywords_list = set(keywords_df['lemmatized_keywords'].tolist())

# if there are punctuations in the keywords list, these punctuation will be kept regardless of puncturation removal step
for word in keywords_list:
    for char in word:
        if char in exclude:
            exclude.remove(char)
            
# Add all words in the given keyword list to pre-defined token dictionary
multi_word = [w.split('_') for w in keywords_list ] 
tokenizer = MWETokenizer(multi_word)


# In[8]:


def lemmatize_text(col): 
    text = col.replace('’', '\'')
    tokens = tokenizer.tokenize(text.split())   
    # remove stop words
    stop_free = ' '.join(w for w in tokens if w.lower() not in stopWords and len(w) > 1)
    # remove punctuation
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    # lemmatize
    lemmas = ' '.join(lemma.lemmatize(word).lower() for word in punc_free.split() if len(lemma.lemmatize(word)) > 1)
    return lemmas.split()

# assign a category based the max number of keywords found in each category
def find_matched_keywords(col):
    keywords_found = []
    for word in col:
        if word in keywords_list:
            keywords_found.append(word) 
    return keywords_found


# ## Read and merge input csv files
pd.options.display.max_rows = 10
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)  
data_df = pd.DataFrame(columns=OUTPUT_COLS)
for filename in filePaths:
    print(filename)    
    df_i = pd.read_csv(filename, encoding = 'utf-8')
    df_x = df_i.dropna(subset=['caption_original']) 
    data_df = data_df.append(df_x, ignore_index=True)



pd.options.display.max_rows = 50
try:
    data_df['lemmatized_text'] = data_df['caption_original'].astype(str).apply(lemmatize_text)
except:
    print('cannot process file...')
data_df['Action_matched_keywords'] = data_df['lemmatized_text'].apply(find_matched_keywords)


pd.options.display.max_rows = 100
output_df = data_df[data_df['Action_matched_keywords'].astype(str) != '[]']
output_df = output_df[OUTPUT_COLS]
output_df.to_csv(outputDir + 'q5q6_merged_ouput_FR_withaddedkeywords.csv', index=None, encoding='utf-8')


# ## Only one line of code is needed to train word embedding model

model = Word2Vec(data_df['lemmatized_text'], size=600, window=50, min_count=20)
# save model
model.save('word2vec_model.bin')
## uncomment the following line of code to load an existing model instead of training a new one.
#model = Word2Vec.load('word2vec_model.bin')
list(model.wv.vocab)


# ## find new action words using existing actions

output_dict = {}
top_n = 30
counter = 1
for keyword in keywords_list:
    try:
        tuple_list = model.wv.most_similar(positive=[keyword], topn=top_n)
    except KeyError:
        print(str(counter) + ': keyword \"' + keyword + '\" is not found...')
        counter += 1
        continue
    new_actions = set(ele[0] for ele in tuple_list if ele not in keywords_list)
    output_dict[keyword] = new_actions
#for x in output_dict:
#    for y in output_dict[x]:
#        print(y)
print(str(counter-1) + ' given keywords not found in the embedding model..')

