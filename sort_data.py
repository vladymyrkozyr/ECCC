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



#for twitter
#rootPath='question answers/question 1/LDA/tw/*.csv'
#rootResultPath_tagged='question answers/question 1/LDA/tw/'
#
##for facebook
#rootPath='question answers/question 1/LDA/fb/posts/*.csv'
#rootResultPath_tagged='question answers/question 1/LDA/fb/posts/'
#
#for instagram
rootPath='question answers/question 1/LDA/in/posts/*.csv'
rootResultPath_tagged='question answers/question 1/LDA/in/posts/'


files = glob.glob(rootPath) 

names = [os.path.basename(x) for x in glob.glob(rootPath)]

keywords_filePath_EN='LDA_classify_topics_with_cleaned_text_en.csv'
keywords_filePath_FR='LDA_classify_topics_with_cleaned_text_fr.csv'

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



#print keywords
#
#print "adsfdfasdfdafadf"
#
#print stemmed_keywords


for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    print name
    print 
         
    categories=[]
    for post in info['caption_cleaned']:
        #print str(post).lower()
        social=0
        economical=0
        environmental=0   
        for social_word, economical_word, environmental_word in zip(stemmed_keywords['Social'],stemmed_keywords['Economical'],stemmed_keywords['Environmental']):
            
            p=str(post).lower()
           # print type(economical_word)
            #print (type(social_word)!='float')
                        
            if isinstance(social_word,six.string_types):
                if social_word in p:
                    social+=1
            if isinstance(economical_word,six.string_types):
                if economical_word in p:
                    economical+=1
            if isinstance(environmental_word,six.string_types):
                if environmental_word in p:
                    environmental+=1
        
        c=max([('Social',social),('Economical',economical),('Environmental',environmental)],key=itemgetter(1))[0]
        m=max([('Social',social),('Economical',economical),('Environmental',environmental)],key=itemgetter(1))
        if m==0:
            categories.append('unknown')
        else:
            categories.append(c)
            
#        print c
#        print social
#        print economical        
#        print environmental
            
    info['category']=categories
    info.to_csv(rootResultPath_tagged+name)        