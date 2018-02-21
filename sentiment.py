# -*- coding: utf-8 -*-
import csv
import pandas
import glob
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from textblob import TextBlob



##for twitter
rootPath='question answers/question 1/tw/*.csv'
rootResultPath='question answers/question 1/tw/'

#for facebook
#rootPath='fb/filtered_data_spell_corrected/comments/*.csv'
#rootResultPath='fb/filtered_data_spell_corrected/comments/'

#for instagram
#rootPath='in/filtered_data_spell_corrected/comments/*.csv'
#rootResultPath='in/filtered_data_spell_corrected/comments/'

files = glob.glob(rootPath)  

names = [os.path.basename(x) for x in glob.glob(rootPath)]

print 'started'

for file, name in zip(files, names):
    if os.path.isfile(rootResultPath+name): 
        accountInfo=pandas.read_csv(file)
        text_sentiment_original_scores=[]
        text_sentiment_original_scores_type=[]
        
        
        
    
        print name
        print
        for text in accountInfo['text_original']: # specify column name containing the text to be cleaned

            #print text
            text_sentiment_original_scores.append(TextBlob(str(text)).sentiment.polarity)    
            
            if TextBlob(str(text)).sentiment.polarity<-0.33333:
                text_sentiment_original_scores_type.append("Negative")                
            if TextBlob(str(text)).sentiment.polarity>0.33333:
                text_sentiment_original_scores_type.append("Positive")
            if (TextBlob(str(text)).sentiment.polarity>-0.33333 and TextBlob(str(text)).sentiment.polarity<0.33333):
                text_sentiment_original_scores_type.append("Neutral")
            
            

        accountInfo['text_sentiment_original_scores']=text_sentiment_original_scores # specify new column name for cleaned text
        accountInfo['text_sentiment_original_scores_type']=text_sentiment_original_scores_type # specify new column name for cleaned text

        
        accountInfo.to_csv(rootResultPath+name)
