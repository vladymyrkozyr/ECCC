
# coding: utf-8
import glob
import os
import pandas as pd
from langdetect import detect
import nltk
#nltk.download()   # comment after first download
from nltk.tokenize import sent_tokenize, MWETokenizer, wordpunct_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import EnglishStemmer
from nltk.probability import FreqDist


### Choose a social media file path

#======= Twitter =======
#rootPath='../tw/cleaned data/*.csv'
#COLUMN_NAME = 'full_text_cleaned'

#======= Facebook =======
#rootPath='../fb/cleaned data/statuses/*.csv'
#COLUMN_NAME = 'status_message_cleaned'

#======= Instagram =======
rootPath='../in/cleaned data/comments/*.csv'
COLUMN_NAME = 'text_cleaned'

filePaths = glob.glob(rootPath)  
multiWordsPath = './multiwords.txt'


stopWords_en = set(stopwords.words('english'))
stopWords_fr = set(stopwords.words('french'))


def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang

 
def filter_stop_words(text):   
    stopWords = stopWords_en  
    if detect_lang(text) == 'fr':
        stopWords = stopWords_fr  
    filtered_text = [w for w in wordpunct_tokenize(text) if w.lower() not in stopWords
            and len(w) > 1 and w.isalnum()]   
    return ' '.join(filtered_text)


def load_multi_words(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        words = [word.strip() for word in lines]
        return words


def tokenize_multi_words(topic_list):
    result = []
    print('>>> Adding custermized topic words/tokens to tokenizer...')
    for words in topic_list:
        print(words)
        result.append(words.split('_'))
    return result



### Load multi-word tokens, tokenize comments/posts, and stem tokens
multiWords = load_multi_words(multiWordsPath)       # load custermized tokens
tokenizedMultiWords = tokenize_multi_words(multiWords)
tokenizer = MWETokenizer(tokenizedMultiWords)
#tokenizer = MWETokenizer()    # Uncomment this line if no customized multi-word tokens needed


def tokenize_text(text):
    return tokenizer.tokenize(text.split()) 


def stem_text(text):
    if detect_lang(text) == 'fr':
        stemmer = FrenchStemmer()
    else:
        stemmer = EnglishStemmer() 
    stems = [stemmer.stem(tok) for tok in text]
    return stems


def main():
    filePaths = glob.glob(rootPath)  
    wordCountOutputDir = os.path.dirname(rootPath).replace('cleaned data', 'filtered_data') + '/word_count/'
    if not os.path.exists(wordCountOutputDir):
        os.makedirs(wordCountOutputDir)  

    for filepath in filePaths:
        filename = os.path.basename(filepath)
        cleanedDataFileName = filepath.replace('cleaned data', 'filtered_data')
        wordCountFileName = wordCountOutputDir + os.path.splitext(filename)[0] + '_word_count.csv'
        print('>>> Processing file: ' + filename)

        df = pd.read_csv(filepath)   # the first unnamed column already exists in csv file 
        df['text_filtered'] = df[COLUMN_NAME].astype(str).apply(filter_stop_words)
        df['text_tokenized'] = df['text_filtered'].apply(tokenize_text)
        df['text_stemmed'] = df['text_tokenized'].apply(stem_text)
        print('>>> Output cleaned data for ' + filename)
        df.to_csv(cleanedDataFileName, index=None) 

        token_lst = df['text_tokenized'].tolist()
        token_fdist = FreqDist()
        for list_i in token_lst:
            list_i = set(list_i)  # Adding this line would count a word once even if it appears multple times in one comment/post
            for token in list_i:
                token_fdist[token.lower()] += 1

        stemmer_lst = df['text_stemmed'].tolist()
        stemmer_fdist = FreqDist()
        for list_i in stemmer_lst:
            list_i = set(list_i)  # Adding this line would count a word once even if it appears multple times in one comment/post
            for token in list_i:
                stemmer_fdist[token.lower()] += 1

        # ## Output token/stemmer frequency distribution
        token_df = pd.DataFrame(list(token_fdist.items()), columns=['token', 'tok_freq'])
        token_df['tok_freq_perc'] = token_df.tok_freq/len(df)
        token_df = token_df.sort_values('tok_freq', ascending=False).reset_index(drop=True)

        stemmer_df = pd.DataFrame(list(stemmer_fdist.items()), columns=['stemmer', 'stem_freq'])
        stemmer_df['stem_freq_perc'] = stemmer_df.stem_freq/len(df)
        stemmer_df = stemmer_df.sort_values('stem_freq', ascending=False).reset_index(drop=True)

        print('>>> Output word frequency distribution for ' + filename)
        output_df = pd.concat([token_df, stemmer_df], axis=1)
        output_df.to_csv(wordCountFileName, index=None)   
        output_df      


if __name__ == '__main__':
    main()
