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


keywords_chosen = './EnglishData/Keywords_ECCC_EN.csv'

# list = [social_media_csv_filepath, cleaned_text_column_name, raw_text_column_name]
data_folder = './EnglishData/Accounts/*.csv'

CSV_COLUMNS = ['caption_cleaned', 'hashtags']

stopWords = set(stopwords.words('english'))
exclude = set(string.punctuation)
exclude.remove('_')
exclude.remove('-')
lemma = WordNetLemmatizer()


def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang


def lemmatize_keywords(col):
    return '_'.join(lemma.lemmatize(word).lower() for word in col.split()) 


def lemmatize_text(row):    
    text_cols = str(row['caption_cleaned']).lower(), str(row['hashtags']).lower()
    normalized_text = []
    if text_cols[0] == 'nan':
        return '', ''
    for text in text_cols:
        if isinstance(text, str):
            tokens = tokenizer.tokenize(text.split())
            
            stop_free = ' '.join(w for w in tokens if w not in stopWords and len(w) > 1)
            punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
            normalized = ' '.join(lemma.lemmatize(word).lower() for word in punc_free.split() if len(lemma.lemmatize(word)) > 2)
            #print(normalized)
            normalized_text.append(normalized.split())
        else:
            normalized_text = ['', '']
    return normalized_text[0], normalized_text[1]


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
  
  # load keywords list
pd.options.display.max_rows = 10
KEYWORD_COL = ['Social', 'Economical', 'Environmental']
keywords_df = pd.read_csv(keywords_chosen, encoding = "ISO-8859-1")
lemma_keywords_df = pd.DataFrame(columns=KEYWORD_COL)
for col in KEYWORD_COL:
    lemma_keywords_df[col] = keywords_df[col].astype(str).apply(lemmatize_keywords)
display(lemma_keywords_df)
soc_list = set(lemma_keywords_df['Social'].tolist())
soc_list.remove('nan')
econ_list = set(lemma_keywords_df['Economical'].tolist())
econ_list.remove('nan')
env_list = set(lemma_keywords_df['Environmental'].tolist())
env_list.remove('nan')
multi_word = [w.split('_') for w in soc_list.union(econ_list).union(env_list) ]   #if '_' in w 
print(multi_word)
tokenizer = MWETokenizer(multi_word)

### To be updated later to save to file
pd.options.display.max_rows = 1000
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)  
for filename in filePaths:
    display(filename)
    #print(os.path.basename(filename))
    data_df = pd.read_csv(filename)
    data_df['lang'] = data_df['caption_cleaned'].astype(str).apply(detect_lang)
    wrong_lang = data_df[data_df['lang'] != 'en'].shape[0]    
    print(wrong_lang/len(data_df))
    data_df['lemmatized_caption_cleaned'], data_df['lemmatized_hashtags']  = zip(*data_df.apply(lemmatize_text, axis=1))
    data_df['keywords_found'], data_df['category'] = zip(*data_df.apply(find_category, axis=1))
    #data_df.to_csv(filename, index=None)
    display(data_df[['words_matched_list', 'lang', 'keywords_found', 'category']])
