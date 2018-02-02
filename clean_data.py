# -*- coding: utf-8 -*-
import preprocessor as p
import csv
import pandas
import glob
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')



rootPath='tw/processed data/*.csv'
rootResultPath='tw/cleaned data/'

files = glob.glob(rootPath)  

names = [os.path.basename(x) for x in glob.glob(rootPath)]

captions=[]

for file, name in zip(files, names):
    accountInfo=pandas.read_csv(file)
    texts=[]
    
    hashtags_matched=[]
    urls_matched=[]
    for text in accountInfo['full_text']: 
        hashtags=[]
        urls=[]
        
        hashtags.append(p.parse(str(text)).hashtags)
        urls.append(p.parse(str(text)).urls)
        
        
        for hashtag, url in zip(hashtags, urls):
            if hashtag:
                buff=[]
                for h in hashtag:
                    buff.append(h.match)
                hashtags_matched.append(buff) 
            else:
                hashtags_matched.append([])
                
            if url:
                buff=[]
                for u in url:    
                    buff.append(u.match)
                urls_matched.append(buff)
            else:
                urls_matched.append([])
            
        texts.append(p.clean((str(text)).encode('utf-8')))

    accountInfo['full_text_cleaned']=texts
    del accountInfo['full_text']
        
    accountInfo['hashtags']=hashtags_matched
    accountInfo['urls']=urls_matched
    accountInfo.to_csv(rootResultPath+name)
    print name

#print p.clean('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

#print p.tokenize('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

#print p.parse('Preprocessor is #awesome 👍 https://github.com/s/preprocessor').hashtags

#l=p.parse('Preprocessor is #awesome 👍 https://github.com/s/preprocessor').hashtags

#print l[0].match
