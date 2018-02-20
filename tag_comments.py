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


#for twitter
#rootPath='tw/filtered_data_spell_corrected/*.csv'
#rootResultPath_tagged='tw/filtered_data_spell_corrected/'

#for facebook
rootPath='fb/filtered_data_spell_corrected/statuses/*.csv'
rootPath_comments='fb/filtered_data_spell_corrected/comments/*.csv'
rootResultPath_tagged='fb/filtered_data_spell_corrected/comments joined with posts/'

#for instagram
#rootPath='in/filtered_data_spell_corrected/posts/*.csv'
#rootPath_comments='in/filtered_data_spell_corrected/comments/*.csv'
#rootResultPath_tagged='in/filtered_data_spell_corrected/comments joined with posts/'


files = glob.glob(rootPath)
files_comments = glob.glob(rootPath_comments) 

names = [os.path.basename(x) for x in glob.glob(rootPath)]

for file, file_comment, name in zip(files, files_comments, names):
    info=pandas.read_csv(file)
    comments=pandas.read_csv(file_comment)
    
    print name
    print 
         
    joined = comments.set_index('status_id').join(info.set_index('status_id'),lsuffix='_comment', rsuffix='_post')     
    joined = joined[joined.columns.drop(list(joined.filter(regex='Unnamed')))]
    joined.to_csv(rootResultPath_tagged+name[:-4]+'_and_comments_joined.csv')     