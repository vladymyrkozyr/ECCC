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

#
##for twitter
#rootPath='../question answers/question 2/tw/*.csv'
#rootResultPath='../question answers/question 2/merging/tw/'

##for facebook
#rootPath='../question answers/question 2/fb/posts/*.csv'
#rootResultPath='../question answers/question 2/merging/fb/'


##for instagram
#rootPath='../question answers/question 2/in/posts/*.csv'
#rootResultPath='../question answers/question 2/merging/in/'

rootPath='../question answers/question 2/merging/*.csv'
rootResultPath='../question answers/question 2/merging/'



files = glob.glob(rootPath)
#files_comments = glob.glob(rootPath_comments)

names = [os.path.basename(x) for x in glob.glob(rootPath)]

##SPLIT DATA
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    
#    info['date_published']=pandas.to_datetime(info['date_published'])
#    
#    period=info['date_published'].dt.to_period('M')
#
#    
#    months = info.groupby([period])
#    
#    print name
#    
#    for month, group in months:
#        group.sort_values(by=['Reactions_SUM'],ascending=False).to_csv(rootResultPath+str(month)+'-'+name)
#        print month        
#



merged = pandas.DataFrame(columns=['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_shares','num_likes','Reactions_SUM','category','language','average_sentiment_score','sentiment'])
for file, name in zip(files, names):
    info=pandas.read_csv(file)
    print name
    print 
    
    merged=merged.append(info.head(5))

merged[['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_shares','num_likes','Reactions_SUM','category','words_matched_list','language','average_sentiment_score','sentiment','account_name']].to_csv('../question answers/question 2/merged.csv')
    