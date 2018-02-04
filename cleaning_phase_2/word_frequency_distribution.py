
# coding: utf-8
import glob
import os
import pandas as pd
from langdetect import detect
import nltk
#nltk.download()   # comment after first download
from nltk.tokenize import MWETokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import EnglishStemmer
from nltk.probability import FreqDist
#from nltk.stem.wordnet import WordNetLemmatizer


### Choose a social media file path

#======= Twitter =======
rootPath='../tw/cleaned data/*.csv'
COLUMN_NAME = 'full_text_cleaned'

#======= Facebook =======
#rootPath='../fb/cleaned data/comments/*.csv'
#COLUMN_NAME = 'comment_message_cleaned'

#======= Instagram =======
#rootPath='../in/cleaned data/posts/*.csv'
#COLUMN_NAME = 'caption'


outputDir = rootPath[:-5] + 'word_count/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


stopWordsPath_en = './stopwords_en.txt'
stopWordsPath_fr = './stopwords_fr.txt'
topicWordsPath = './topicwords.txt'



def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang


def load_stop_words(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        words = [token.strip() for token in lines]    # .encode('utf8')
        print('>>> Loading stopwords... ')
        return words

stopWords_en = set(load_stop_words(stopWordsPath_en))
stopWords_fr = set(load_stop_words(stopWordsPath_fr))

   
def filter_stop_words(text):   ##  Why not working????????????
    stopWords = stopWords_en  # use global set variable 
    if detect_lang(text) == 'fr':
        stopWords = stopWords_fr
    filtered_text = []
    for word in text.split():
        if word.lower() not in stopWords: 
            #print(word.lower())
            filtered_text.append(word.strip())
    return ' '.join(filtered_text)


def filter_nonascii_chars(text):   #some non ascii chars are important! 
    keep_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                  'é', 'à', 'è', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ç', 'ë', 'ï', 'ü', 
                  ' ', '\''}
    filtered_text = []
    for word in text:
        if word in keep_chars:  
            filtered_text.append(word)
    return ''.join(filtered_text)


def load_topic_words(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        words = [word.strip() for word in lines]
        return words


def tokenize_topic_words(topic_list):
    result = []
    print('>>> Adding custermized topic words/tokens to tokenizer...')
    for words in topic_list:
        print(words)
        result.append(words.split('_'))
    return result



### Load multi-word tokens, tokenize comments/posts, and stem tokens
topicWords = load_topic_words(topicWordsPath)       # load custermized tokens
tokenizedTopicWords = tokenize_topic_words(topicWords)
tokenizer = MWETokenizer(tokenizedTopicWords)
#tokenizer = MWETokenizer()    # Uncomment this line if no customized multi-word tokens needed


def tokenize_text(text):
    return tokenizer.tokenize(text.lower().split()) 


def stem_text(text):
    if detect_lang(text) == 'fr':
        stemmer = FrenchStemmer()
    else:
        stemmer = EnglishStemmer() 
    stems = [stemmer.stem(tok) for tok in text]
    return stems


"""
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(tok) for tok in text]
    print(lemmas)
    return lemmas
"""

def main():
    filePaths = glob.glob(rootPath)  
    for filepath in filePaths:
        filename = os.path.basename(filepath)
        outputFileName = filename[:-4] + '_word_count.csv'


        df = pd.read_csv(filepath)   # the first unnamed column already exists in csv file 
        df['text_filtered'] = df[COLUMN_NAME].astype(str)
        df['text_filtered1'] = df['text_filtered'].apply(filter_stop_words)
        df['text_filtered2'] = df['text_filtered1'].apply(filter_nonascii_chars)
        df['text_filtered3'] = df['text_filtered2'].apply(filter_stop_words)
        df[['text_filtered1', 'text_filtered2', 'text_filtered3']]


        df['text_tokenized'] = df['text_filtered2'].apply(tokenize_text)
        df['text_stemmed'] = df['text_tokenized'].apply(stem_text)


        token_lst = df['text_tokenized'].tolist()
        token_fdist = FreqDist()
        for list_i in token_lst:
            list_i = set(list_i)  # Adding this line would count a word once even if it appears multple times in one comment/post
            for token in list_i:
                token_fdist[token.lower()] += 1
        token_fdist.most_common(30)

        stemmer_lst = df['text_stemmed'].tolist()
        stemmer_fdist = FreqDist()
        for list_i in stemmer_lst:
            list_i = set(list_i)  # Adding this line would count a word once even if it appears multple times in one comment/post
            for token in list_i:
                stemmer_fdist[token.lower()] += 1
        stemmer_fdist.most_common(30)

        # ## Output token/stemmer frequency distribution
        token_df = pd.DataFrame(list(token_fdist.items()), columns=['token', 'tok_freq'])
        token_df['tok_freq_perc'] = token_df.tok_freq/len(df)
        token_df = token_df.sort_values('tok_freq', ascending=False).reset_index(drop=True)

        stemmer_df = pd.DataFrame(list(stemmer_fdist.items()), columns=['stemmer', 'stem_freq'])
        stemmer_df['stem_freq_perc'] = stemmer_df.stem_freq/len(df)
        stemmer_df = stemmer_df.sort_values('stem_freq', ascending=False).reset_index(drop=True)

        print('>>> Output word frequency distribution for ' + filename)
        output_df = pd.concat([token_df, stemmer_df], axis=1)
        output_df.to_csv(outputDir + outputFileName, index=None)      


if __name__ == '__main__':
    main()
