
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd

from langdetect import detect
#nltk.download()   # comment after first download
from nltk.tokenize import wordpunct_tokenize, MWETokenizer
from nltk.corpus import stopwords
import string
import operator
from FrenchLefffLemmatizer.FrenchLefffLemmatizer import FrenchLefffLemmatizer


pd.options.display.max_rows = 30


# In[2]:


keywords_chosen = 'Keywords_ECCC_FR.csv'

data_folder = './Accounts/*.csv'

CSV_COLUMNS = ['caption_original', 'hashtags']


# In[3]:


outputDir = os.path.dirname(data_folder) + '/output/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


# In[4]:


exclude = set(string.punctuation)


# In[5]:


stopWords = set(stopwords.words('french'))
lemma = FrenchLefffLemmatizer()


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


# In[7]:


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

punc_keep = set()
for word in keywords_list:
    for char in word:
        if char in exclude:
            punc_keep.add(char)

for punc in punc_keep:
    exclude.remove(punc)

multi_word = [w.split('_') for w in keywords_list ]   #if '_' in w 
tokenizer = MWETokenizer(multi_word)


# In[8]:


def lemmatize_text(row):
    # we are using the original text in the caption_original column because
    # the script we originally used to clean the data didn't handle the French
    # text correctly and so the results in the caption_cleaned and hashtags
    # columns are corrupted and should not be used
    # however all the cleaning (tokenizing, removal of unnecessary punctuation,
    # and lemmatization is now done right here in this script and it's done
    # correctly for French
    text = str(row['caption_original']).replace('nan', '')
    #caption_cleaned =  str(row['caption_cleaned']).replace('nan', '')
    """hashtags = str(row['hashtags'])
    hashtags = hashtags.replace('[', '')
    hashtags = hashtags.replace(']', '')
    hashtags = hashtags.replace('\'', '')
    hashtags = hashtags.replace(',', '')
    text = hashtags + ' '+ caption_original"""
    #print(text)
    text = text.replace('’', '\'')
    tokens = tokenizer.tokenize(text.split())            
    stop_free = ' '.join(w for w in tokens if w not in stopWords and len(w) > 1)
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    lemmas = ' '.join(lemma.lemmatize(word).lower() for word in punc_free.split() if len(lemma.lemmatize(word)) > 2)
    stop_free_2 = ' '.join(w for w in lemmas.split() if w not in stopWords and len(w) > 1)
    #print(stop_free_2)
    return stop_free_2.split()


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


# In[9]:


pd.options.display.max_rows = 100
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)  
for filename in filePaths:
    print(filename)
    basename = os.path.basename(filename)
    outputFileName = outputDir + basename
    data_df = pd.read_csv(filename, encoding = 'utf-8')
    # drop these columns from the input data which come from previous analysis
    # and should be ignored
    data_df = data_df.drop(['category','words_matched_list'], axis=1)
    if data_df.shape[0] < 1:
        data_df.to_csv(outputFileName, index=None) 
        continue
    data_df['lang'] = data_df['caption_original'].astype(str).apply(detect_lang)
    #wrong_lang = data_df[data_df['lang'] != 'fr'].shape[0]
    data_df['lemmatized_text'] = data_df.apply(lemmatize_text, axis=1)
    data_df['matched_keywords'], data_df['category'] = zip(*data_df.apply(find_category, axis=1))
    
    #display(data_df[['words_matched_list', 'lemmatized_text','matched_keywords', 'category']])
    output_list = data_df.columns.tolist()
    #output_list.remove('words_matched_list')
    output_list.remove('lang')
    #output_list.remove('lemmatized_text')
    output_list.append('category')
    output_df = data_df[output_list]
    output_df.to_csv(outputFileName, index=None)    


# In[9]:


#print(stopWords)

