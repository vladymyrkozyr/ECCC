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
import six
reload(sys)
sys.setdefaultencoding('utf8')

def detect_lang(text):
    try:
        lang = detect(text)
    except:
        return 'error'
    return lang


def stem_text(text):
    if detect_lang(text) == 'fr':
        stemmer = FrenchStemmer()
    else:
        stemmer = EnglishStemmer() 
    return stemmer.stem(text)
   # stems = [stemmer.stem(tok) for tok in text]
   # return stems



##for twitter
#rootPath='question answers/question 1/keywords classification/tw/*.csv'
#rootResultPath_tagged='question answers/question 1/keywords classification/tw/'


##for facebook
#rootPath='question answers/question 1/keywords classification/fb/posts/*.csv'
#rootResultPath_tagged='question answers/question 1/keywords classification/fb/posts/'


#for instagram
rootPath='question answers/question 1/keywords classification/in/posts/*.csv'
rootResultPath_tagged='question answers/question 1/keywords classification/in/posts/'


files = glob.glob(rootPath) 

names = [os.path.basename(x) for x in glob.glob(rootPath)]

keywords_filePath_EN='Keywords_ECCC_EN.csv'
keywords_filePath_FR='Keywords_ECCC_FR.csv'

keywords=pandas.concat([pandas.read_csv(keywords_filePath_EN,engine='python'),pandas.read_csv(keywords_filePath_FR,engine='python')])
stemmed_keywords=keywords

social_column=[]
economical_column=[]
environmental_column=[]

#for soc, eco, env in zip(keywords['Social'],keywords['Economical'],keywords['Environmental']):
#    social_column.append(stem_text((soc)))
#    economical_column.append(stem_text((eco)))
#    environmental_column.append(stem_text((env)))

#print social_column
#print economical_column
#print environmental_column
#print len(social_column)
#print len(economical_column)
#print len(environmental_column)
stemmed_keywords['Social']=keywords['Social']
stemmed_keywords['Economical']=keywords['Economical']
stemmed_keywords['Environmental']=keywords['Environmental']


for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    print name
    print 
         
    categories=[]
    keywords_list=[]
    sentiments=[]
    for post, sentiment in zip(info['caption_cleaned'],info['average_sentiment_score']):
        
        social=0
        economical=0
        environmental=0   
        
        soc_list=[]
        eco_list=[]
        env_list=[]
        
        if sentiment==0:
            sentiments.append('neutral')
        if sentiment>0:
            sentiments.append('positive')
        if sentiment<0:
            sentiments.append('negative')
        
        for social_word, economical_word, environmental_word in zip(stemmed_keywords['Social'],stemmed_keywords['Economical'],stemmed_keywords['Environmental']):
            
            p=str(post).lower()
           # print type(economical_word)
            #print (type(social_word)!='float')
                        
            if isinstance(social_word,six.string_types):
                if social_word in p:
                    social+=1
                    soc_list.append(social_word)
            if isinstance(economical_word,six.string_types):
                if economical_word in p:
                    economical+=1
                    eco_list.append(economical_word)
            if isinstance(environmental_word,six.string_types):
                if environmental_word in p:
                    environmental+=1
                    env_list.append(environmental_word)
        
        c=max([('Social',social,soc_list),('Economical',economical,eco_list),('Environmental',environmental,env_list)],key=itemgetter(1))[0]
        
        m=max([('Social',social,soc_list),('Economical',economical,eco_list),('Environmental',environmental,env_list)],key=itemgetter(1))
        
        l=max([('Social',social,soc_list),('Economical',economical,eco_list),('Environmental',environmental,env_list)],key=itemgetter(1))[2]
        
        if len(l)==0:
            categories.append('unknown')
            keywords_list.append('')
        else:
            categories.append(c)            
            keywords_list.append(list(set(l)))
    
            
            #', '.join(set(l))
            
    info['category']=categories
    info['words_matched_list']=keywords_list
    info['sentiment']=sentiments
    info.to_csv(rootResultPath_tagged+name)   
    
    # CLEAN UNNAMED COLUMNS

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    
    print name
    print 
                                   
    info = info[info.columns.drop(list(info.filter(regex='Unnamed')))]

    info.to_csv(rootResultPath_tagged+name)        