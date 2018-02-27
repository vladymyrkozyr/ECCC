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
rootPath='../question answers/question 1/keywords classification/tw/*.csv'
rootResultPath='../question answers/question 1/keywords classification/tw/'


##for facebook
#rootPath='../question answers/question 1/keywords classification/fb/posts/*.csv'
#rootPath_comments='../question answers/question 1/keywords classification/fb/comments/*.csv'
#rootResultPath='../question answers/question 1/keywords classification/fb/posts/'


##for instagram
#rootPath='../question answers/question 1/keywords classification/in/posts/*.csv'
#rootPath_comments='../question answers/question 1/keywords classification/in/comments/*.csv'
#rootResultPath='../question answers/question 1/keywords classification/in/posts/'


files = glob.glob(rootPath) 
#files_comments = glob.glob(rootPath_comments) 

names = [os.path.basename(x) for x in glob.glob(rootPath)]

keywords_filePath_EN='../Keywords_ECCC_EN.csv'
keywords_filePath_FR='../Keywords_ECCC_FR.csv'

keywords=pandas.concat([pandas.read_csv(keywords_filePath_EN,engine='python'),pandas.read_csv(keywords_filePath_FR,engine='python')])
stemmed_keywords=keywords

social_column=[]
economical_column=[]
environmental_column=[]

stemmed_keywords['Social']=keywords['Social']
stemmed_keywords['Economical']=keywords['Economical']
stemmed_keywords['Environmental']=keywords['Environmental']


#LANGUAGE

#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    #comments=pandas.read_csv(file_comment)
#    
#    print name
#    print 
#    
#    info['language']=info['text_tokenized'].apply(detect_lang)
##    del info['text_sentiment_original_scores']
##    del info['text_sentiment_original_scores_type']
#    
#    info.to_csv(rootResultPath+name)



#
## SENTIMENT AVERAGE
#
#
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
#            if post['status_id']==comment['status_id']:
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
    
##RENAME COLS
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    #comments=pandas.read_csv(file_comment)
#    
#    
#    print name
#    print 
#    
#    #info=info.rename(index=str, columns={"score": "Reactions_SUM"})
#    print info
#    #info['Reactions_SUM']=info['retweet_count']+info['favorite_count']
#    info['Reactions_SUM']=info['num_reactions']+info['num_comments']+info['num_shares']    
#    #info['Reactions_SUM']=info['likes']+info['comments']
#    
#    #info=info.sort_values(by=['score'],ascending=False)
#    
#    
#    info.to_csv(rootResultPath+name)
    
## SCORE
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
#    #info['score']=info['num_reactions']+info['num_comments']+info['num_shares']    
#    #info['score']=info['likes']+info['comments']
#    
#    info=info.sort_values(by=['Reactions_SUM'],ascending=False)
#    
#    
#    info.to_csv(rootResultPath+name)


# CLEAN DATA
#for file, name in zip(files, names):
#    info=pandas.read_csv(file)
#    #comments=pandas.read_csv(file_comment)
#    
##    #facebook
##    account_name=[name[:-13]]*len(info)
##    
##    print account_name
##
##    info=info.rename(index=str, columns={"status_id": "id","status_published":"date_published","status_link":"link","text_original":"caption_original","status_message_cleaned":"caption_cleaned"})   
##    cleaned_data=info[['id','date_published','link','caption_original','caption_cleaned','hashtags','num_reactions','num_comments','num_shares','num_likes','num_loves','num_wows','num_hahas','num_sads','num_angrys','num_special','Reactions_SUM','category','language','average_sentiment_score']]
#
#    #twitter
#    account_name=[name[:-5]+"er"]*len(info)
#
#    print account_name
#    info=info.rename(index=str, columns={"created_at":"date_published",
#                                         "urls":"link",
#                                         "text_original":"caption_original",
#                                         "text_filtered":"caption_cleaned",
#                                         "text_sentiment_original_scores":"average_sentiment_score",
#                                        "text_sentiment_original_scores_type":"sentiment",
#                                         "retweet_count":"num_shares",
#                                         "favorite_count":"num_likes"
#                                        })
#
#    cleaned_data=info[['id','date_published','link','caption_original','caption_cleaned','hashtags','num_shares','num_likes','Reactions_SUM','category','language','average_sentiment_score','sentiment']]

#    #instagram
#    account_name=[name[:-9]+"instagram"]*len(info)
##    
#    print account_name
#    info=info.rename(index=str, columns={"date":"date_published",
#                                         "url":"link",
#                                         "caption":"caption_original",
#                                         "text_filtered":"caption_cleaned",
#                                        "caption_hashtags":"hashtags",
#                                        "comments":"num_comments",
#                                        "likes":"num_likes"})
#
#    cleaned_data=info[['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments','num_likes','Reactions_SUM','category','language','average_sentiment_score']]
#    
#    cleaned_data['account_name']=account_name
#    
#    cleaned_data.to_csv(rootResultPath+name)

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    print name
    print 
         
    categories=[]
    keywords_list=[]
#    sentiments=[]
    for post, sentiment in zip(info['caption_cleaned'],info['average_sentiment_score']):
        
        social=0
        economical=0
        environmental=0   
        
        soc_list=[]
        eco_list=[]
        env_list=[]
#        
#        if sentiment==0:
#            sentiments.append('neutral')
#        if sentiment>0:
#            sentiments.append('positive')
#        if sentiment<0:
#            sentiments.append('negative')
        
        for social_word, economical_word, environmental_word in zip(stemmed_keywords['Social'],stemmed_keywords['Economical'],stemmed_keywords['Environmental']):
            
            p=str(post).lower()
                        
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
            
    info['category']=categories
    info['words_matched_list']=keywords_list
#    info['sentiment']=sentiments
    info.to_csv(rootResultPath+name)   

# CLEAN UNNAMED COLUMNS

for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    
    print name
    print 
                                   
    info = info[info.columns.drop(list(info.filter(regex='Unnamed')))]
          
    info.to_csv(rootResultPath+name)

    