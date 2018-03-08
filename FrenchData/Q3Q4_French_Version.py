
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd
from langdetect import detect
#nltk.download()   # comment after first download
from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
import string
import operator
from FrenchLefffLemmatizer.FrenchLefffLemmatizer import FrenchLefffLemmatizer


# In[2]:


keywords_chosen = '13_FSDS_Goals_Keywords_FR.csv'

data_folder = './Accounts/q1_output/*.csv'

CSV_COLUMNS = ['caption_original', 'hashtags']


# create output directory
outputDir = './Accounts/q3q4_output/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


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


# load keywords list
pd.options.display.max_rows = 100
keywords_df = pd.read_csv(keywords_chosen, encoding='utf-8')   # "ISO-8859-1"
KEYWORDS_COLS = keywords_df.columns
lemma_keywords_df = pd.DataFrame(columns=KEYWORDS_COLS)

# category_dict is a dictionary that holds
category_dict = {}
keywords_list = set()
# for each column in the keywords lists:
#   lemma_keywords_df gets a column that contains the lemmatized version of what's in the keyword list
#   category_dict gets a key with value the set of all lemmatized keywords for that FSDS goal
for col in KEYWORDS_COLS:
    lemma_keywords_df[col] = keywords_df[col].astype(str).apply(lemmatize_keywords)
    category_dict[col] = set(lemma_keywords_df[col].tolist())
    try:
        category_dict[col].remove('')
    except:
        pass
    # keywords_list is the set of alllll the keywords
    keywords_list = keywords_list.union(category_dict[col])


# if there are punctuations in the keywords list, these punctuation will be kept regardless of puncturation removal step
for word in keywords_list:
    for char in word:
        if char in exclude:
            exclude.remove(char)
            
# Add all words in the given keyword list to pre-defined token dictionary
multi_word = [w.split('_') for w in keywords_list ]   #if '_' in w 
tokenizer = MWETokenizer(multi_word)


def lemmatize_text(row):
    # we are using the original text in the caption_original column because
    # the script we originally used to clean the data didn't handle the French
    # text correctly and so the results in the caption_cleaned and hashtags
    # columns are corrupted and should not be used
    # however all the cleaning (tokenizing, removal of unnecessary punctuation,
    # and lemmatization is now done right here in this script and it's done
    # correctly for French
    
    text = str(row['caption_original']).replace('nan', '')
    text = text.replace('’', '\'')
    tokens = tokenizer.tokenize(text.split())

    # remove stop words
    stop_free = ' '.join(w for w in tokens if w not in stopWords and len(w) > 1)

    # remove punctuation
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)

    # lemmatize
    lemmas = ' '.join(lemma.lemmatize(word).lower() for word in punc_free.split() if len(lemma.lemmatize(word)) > 1)

    # remove stop words that appear after lemmatization
    stop_free_2 = ' '.join(w for w in lemmas.split() if w not in stopWords and len(w) > 1)

    return stop_free_2.split()


# assign a category based on the max number of keywords found in each category
def find_category(row):
    text = row['lemmatized_text']
    keywords_found = []

    # counter is a dictionary with a key for each of the 13 FSDS goals,
    # ie; for each column in the keyword list
    # it will hold the count for this row of keywords matched for each of the FSDS goals
    counter = {}
    for col in KEYWORDS_COLS:
        counter[col] = 0

    # initialize category to unknown
    category = 'unknown'

    # for each word in the lemmatized text, go through each column of the keyword list
    for word in text:
        for col in KEYWORDS_COLS:
            # if the word is in the set of lemmatized keywords for that FSDS goal
            #     add it to the list of keywords found
            #     increment the counter for this FSDS goal
            if word in category_dict[col]:
                keywords_found.append(word)
                counter[col] += 1
    if len(keywords_found) > 0:
        category = max(counter.items(), key=operator.itemgetter(1))[0]    
    return keywords_found, category


pd.options.display.max_rows = 10

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

    #data_df = data_df.drop(['category', 'words_matched_list'], axis=1)
    data_df.fillna('')

    try:
        data_df['lemmatized_text'] = data_df.apply(lemmatize_text, axis=1)
    except:
        print('cannot process file: ' + basename)
        continue

    data_df['FSDS_matched_keywords'], data_df['FSDS_category'] = zip(*data_df.apply(find_category, axis=1))

    output_list = data_df.columns.tolist()
    #output_list.remove('lemmatized_text')
    output_df = data_df[output_list]
    output_df.to_csv(outputFileName, encoding='utf-8', index=None)    
    