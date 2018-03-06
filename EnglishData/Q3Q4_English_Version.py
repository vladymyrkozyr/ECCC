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


##for twitter
rootPath='../question answers/question 3 and 4/tw/*.csv'
rootResultPath_tagged='../question answers/question 3 and 4/tw/'


##for facebook
#rootPath='../question answers/question 3 and 4/fb/posts/*.csv'
#rootResultPath_tagged='../question answers/question 3 and 4/fb/posts/'


##for instagram
#rootPath='../question answers/question 3 and 4/in/posts/*.csv'
#rootResultPath_tagged='../question answers/question 3 and 4/in/posts/'


files = glob.glob(rootPath) 

names = [os.path.basename(x) for x in glob.glob(rootPath)]

keywords_filePath_EN='../13_FSDS_Goals_Keywords_EN.csv'
keywords_filePath_FR='../13_FSDS_Goals_Keywords_FR.csv'

keywords=pandas.concat([pandas.read_csv(keywords_filePath_EN,engine='python'),pandas.read_csv(keywords_filePath_FR,engine='python')])
stemmed_keywords=keywords



for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    print name
    print 
    
    FSDS_Goal_Category=[]
    FSDS_Goal_Category_word_list=[]
    
    for post in info['caption_cleaned']:
                
        list_of_tuples=[]
        for column in stemmed_keywords:
            score=0
            word_list=[]
            for word in stemmed_keywords[column]:                
                p=str(post).lower()
                if isinstance(word,six.string_types):
                    if word in p:
                        score+=1
                        word_list.append(word)
            list_of_tuples.append((str(column),score,word_list))
            
            
        c=max(list_of_tuples,key=itemgetter(1))[0]
            
        m=max(list_of_tuples,key=itemgetter(1))
       
        l=max(list_of_tuples,key=itemgetter(1))[2]

        if len(l)==0:
            FSDS_Goal_Category.append('unknown')
            FSDS_Goal_Category_word_list.append('')
        else:
            FSDS_Goal_Category.append(c)            
            FSDS_Goal_Category_word_list.append(list(set(l)))
    

    
    info['FSDS_Goal_Category']=FSDS_Goal_Category
    info['FSDS_Goal_Category_word_list']=FSDS_Goal_Category_word_list
    info.to_csv(rootResultPath_tagged+name)   
    
    # CLEAN UNNAMED COLUMNS

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    
    print name
    print 
                                   
    info = info[info.columns.drop(list(info.filter(regex='Unnamed')))]

    info.to_csv(rootResultPath_tagged+name)        