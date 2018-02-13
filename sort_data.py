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
#rootPath='tw/filtered_data_spell_corrected/*.csv'
#rootResultPath='tw/filtered_data_spell_corrected/'

#for facebook
rootPath='fb/filtered_data_spell_corrected/statuses/*.csv'
rootResultPath='fb/filtered_data_spell_corrected/comments/'

#for instagram
#rootPath='in/filtered_data_spell_corrected/posts/*.csv'
#rootResultPath='in/filtered_data_spell_corrected/comments/'

files = glob.glob(rootPath)  

names = [os.path.basename(x) for x in glob.glob(rootPath)]

keywords_filePath='Keywords_ECCC.csv'

keywords=pandas.read_csv(keywords_filePath)

print keywords


for file, name in zip(files, names):
    info=pandas.read_csv(file)
    
    print name
    print
    for post in info['text_original']:
        print str(post).lower()
        social=0
        economical=0
        environmental=0
        for social_word, economical_word, environmental_word in zip(keywords['Social'],keywords['Economical'],keywords['Environmental']):
            
#            print social_word
#            print economical_word
#            print environmental_word
            if str(social_word).lower() in str(post).lower() and str(social_word).lower()!='nan':
                social+=1
            if str(economical_word).lower() in str(post).lower() and str(economical_word).lower()!='nan':
                economical+=1
            if str(environmental_word).lower() in str(post).lower() and str(environmental_word).lower()!='nan':
                environmental+=1
        
        print ('social: '+str(social))
        print ('economical: '+str(economical))
        print ('environmental: '+str(environmental))
    break

print 'started'

#for file, name in zip(files, names):
#    accountInfo=pandas.read_csv(file)
#    print name
#    print
#    for text in accountInfo['text_original']:
        