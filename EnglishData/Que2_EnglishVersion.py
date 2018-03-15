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


rootPath='Accounts/q2_output/months/*.csv'
rootResultPath='Accounts/q2_output/'




files = glob.glob(rootPath)
#files_comments = glob.glob(rootPath_comments)

names = [os.path.basename(x) for x in glob.glob(rootPath)]

#Merge all DATA
#merged = pandas.DataFrame(columns=['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_shares','num_likes','Reactions_SUM','category','matched_keywords','language','average_sentiment_score','sentiment'])
#
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    merged=merged.append(info)
##    info['date_published']=pandas.to_datetime(info['date_published'])
##    
##    period=info['date_published'].dt.to_period('M')
##
##    
##    months = info.groupby([period])
##    
##    print name
##    
##    for month, group in months:
##        group.sort_values(by=['Reactions_SUM'],ascending=False).to_csv(rootResultPath+str(month)+'-'+name)
##        print month        
#merged[['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_shares','num_likes','Reactions_SUM','category','matched_keywords','language','average_sentiment_score','sentiment','account_name']].to_csv(rootResultPath+'merged_ALL.csv')

#########################################################3

#info=pandas.read_csv('Accounts/q2_output/merged_ALL.csv')
#info['date_published']=pandas.to_datetime(info['date_published'])
#period=info['date_published'].dt.to_period('M')
#
#    
#months = info.groupby([period])   
#
#    
#for month, group in months:
#    group.sort_values(by=['Reactions_SUM'],ascending=False).to_csv(rootResultPath+str(month)+'.csv')
#    print month    



merged = pandas.DataFrame(columns=['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_shares','num_likes','Reactions_SUM','category','matched_keywords','language','average_sentiment_score','sentiment'])

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    print name
    print 
    
    merged=merged.append(info.head(3))

merged[['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_shares','num_likes','Reactions_SUM','category','matched_keywords','language','average_sentiment_score','sentiment','account_name']].to_csv(rootResultPath+'merged_TOP3_monthly.csv')
    
