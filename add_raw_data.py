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
rootPath='tw/filtered_data/*.csv'
rootResultPath='tw/filtered_data_spell_corrected/'

rootPath_raw='tw/processed data/*.csv'

#for facebook
#rootPath='fb/filtered_data/comments/*.csv'
#rootResultPath='fb/filtered_data_spell_corrected/comments/'
#
#rootPath_raw='fb/processed data/comments/*.csv'

#for instagram
#rootPath='in/filtered_data/posts/*.csv'
#rootResultPath='in/filtered_data_spell_corrected/posts/'
#
#rootPath_raw='in/processed data/posts/*.csv'


files = glob.glob(rootPath) 
files_raw=glob.glob(rootPath_raw)

names = [os.path.basename(x) for x in glob.glob(rootPath)]

print 'started'

for file, file_raw, name in zip(files, files_raw, names):
    #if os.path.isfile(rootResultPath+name): 
    accountInfo=pandas.read_csv(file)
    accountInfo_raw=pandas.read_csv(file_raw)

    print name
    print

    accountInfo['text_original']=accountInfo_raw['full_text'] # specify new column name for cleaned text

    accountInfo.to_csv(rootResultPath+name)
