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


##for twitter
#rootPath='../question answers/question 1/tw/*.csv'
#rootResultPath='../question answers/question 2/tw/'

#for facebook
#rootPath='../question answers/question 1/fb/posts/*.csv'
#rootPath_comments='../question answers/question 1/fb/comments/*.csv'
#rootResultPath='../question answers/question 2/fb/posts/'


#for instagram
rootPath='../question answers/question 1/in/posts/*.csv'
rootPath_comments='../question answers/question 1/in/comments/*.csv'
rootResultPath='../question answers/question 2/in/posts/'




files = glob.glob(rootPath)
#files_comments = glob.glob(rootPath_comments)

names = [os.path.basename(x) for x in glob.glob(rootPath)]

# CLEAN DATA
for file, name in zip(files, names):
    info=pandas.read_csv(file)
    #comments=pandas.read_csv(file_comment)
    
    #facebook
#    account_name=[name[:-13]]*len(info)
#    
#    print account_name

#    info=info.rename(index=str, columns={"status_id": "id","status_published":"date_published","status_link":"link","text_original":"caption_original","status_message_cleaned":"caption_cleaned"})
#    cleaned_data=info[['id','date_published','link','caption_original','caption_cleaned','hashtags','category','Reactions_SUM','average_sentiment_score','language']]
#    
#    cleaned_data['account_name']=account_name

    #twitter
#    account_name=[name[:-5]+"er"]*len(info)
##    
#    print account_name
#    info=info.rename(index=str, columns={"created_at":"date_published",
#                                         "urls":"link",
#                                         "text_original":"caption_original",
#                                         "text_filtered":"caption_cleaned",
#                                         "sentiment_score":'average_sentiment_score'})
#    cleaned_data=info[['id','date_published','link','caption_original','caption_cleaned','hashtags','category','Reactions_SUM','average_sentiment_score','language']]
#    
#    cleaned_data['account_name']=account_name

    #instagram
    account_name=[name[:-9]+"instagram"]*len(info)
#    
    print account_name
    info=info.rename(index=str, columns={"mediaid": "id",  
                                        "date":"date_published",
                                         "url":"link",
                                         "caption":"caption_original",
                                         "text_filtered":"caption_cleaned",
                                        "caption_hashtags":"hashtags"})
    cleaned_data=info[['id','date_published','link','caption_original','caption_cleaned','hashtags','category','Reactions_SUM','average_sentiment_score','language']]
    
    cleaned_data['account_name']=account_name
    
    cleaned_data.to_csv(rootResultPath+name)


#SPLIT DATA
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    #comments=pandas.read_csv(file_comment)
#    
#    info['status_published']=pandas.to_datetime(info['status_published'])
#    
#    period=info['status_published'].dt.to_period('M')
#    
#    print info['status_published']
#    
#    months = info.groupby([period])
#    
#    for month, group in months:
#        print group.sort_values(by=['Reactions_SUM'],ascending=False)
#    
#    print name
#    print 
#    print months
#    
#    break
##    info.to_csv(rootResultPath+name)

    