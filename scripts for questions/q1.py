# -*- coding: utf-8 -*-
import csv
import pandas
import glob
import os
import sys
from textblob import TextBlob
import nltk
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import EnglishStemmer
from langdetect import detect
from operator import itemgetter
from statistics import mean
import six
reload(sys)
sys.setdefaultencoding('utf8')


def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang


#for twitter
#rootPath='../question answers/question 1/tw/*.csv'
#rootResultPath='../question answers/question 1/tw/'

#for facebook
rootPath='../question answers/question 1/fb/posts/*.csv'
rootPath_comments='../question answers/question 1/fb/comments/*.csv'
rootResultPath='../question answers/question 1/fb/posts/'


#for instagram
#rootPath='../question answers/question 1/in/posts/*.csv'
#rootPath_comments='../question answers/question 1/in/comments/*.csv'
#rootResultPath='../question answers/question 1/in/posts/'




files = glob.glob(rootPath)
files_comments = glob.glob(rootPath_comments)

names = [os.path.basename(x) for x in glob.glob(rootPath)]

#LANGUAGE

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    #comments=pandas.read_csv(file_comment)
    
    print name
    print 
    
    info['language']=info['text_tokenized'].apply(detect_lang)
#    del info['text_sentiment_original_scores']
#    del info['text_sentiment_original_scores_type']
    
    info.to_csv(rootResultPath+name)


# SCORE
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    #comments=pandas.read_csv(file_comment)
#    
#    
#    print name
#    print 
#    
#    
#    #info['score']=info['retweet_count']+info['favorite_count']
#    info['score']=info['num_reactions']+info['num_comments']+info['num_shares']    
#    #info['score']=info['likes']+info['comments']
#    
#    info=info.sort_values(by=['score'],ascending=False)
#    
#    
#    info.to_csv(rootResultPath+name)

# SENTIMENT AVERAGE


#for file, file_comment, name in zip(files, files_comments, names):
#    info=pandas.read_csv(file)
#    comments=pandas.read_csv(file_comment)
#    
#    scored_posts=pandas.DataFrame()
#    print name
#    print
#    
#    average_sentiment_score=[]
#    
#    for i, post in info.iterrows():
#        sentiment_score=[]
#        print post
#        #x=raw_input()
#        for j, comment in comments.iterrows():
#            if post['id']==comment['post_id']:
#                sentiment_score.append(comment['text_sentiment_original_scores'])
#        if len(sentiment_score)!=0:
#            #print sentiment_score
#            average_sentiment_score.append(mean(sentiment_score))
#        else:
#            average_sentiment_score.append(0)
#    
#    info['average_sentiment_score']=average_sentiment_score
#
#    info.to_csv(rootResultPath+name) 
    
# RENAME COLS
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    #comments=pandas.read_csv(file_comment)
#    
#    
#    print name
#    print 
#    
#    info=info.rename(index=str, columns={"text_sentiment_original_scores": "sentiment_score", "text_sentiment_original_scores_type": "sentiment_type"})
#    print info
#    #info['score']=info['retweet_count']+info['favorite_count']
#    #info['score']=info['num_reactions']+info['num_comments']+info['num_shares']    
#    #info['score']=info['likes']+info['comments']
#    
#    #info=info.sort_values(by=['score'],ascending=False)
#    
#    
#    info.to_csv(rootResultPath+name)

# CLEAN UNNAMED COLUMNS

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    #comments=pandas.read_csv(file_comment)
    
    
    print name
    print 
                                   
    info = info[info.columns.drop(list(info.filter(regex='Unnamed')))]
          
    info.to_csv(rootResultPath+name)

    