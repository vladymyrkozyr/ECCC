# -*- coding: utf-8 -*-
import preprocessor as p
import csv
import pandas

file=pandas.read_csv('in/processed data/posts/parks.canada_posts.csv')

#print file['caption']

captions=[]

file=file.replace('\n','',regex=True)

#for caption in file['caption']:    
#    captions.append(p.clean(caption).encode('utf-8'))

#file['caption']=captions
print file['caption']

file.to_csv('in/cleaned data/posts/parks.canada_posts.csv')

#print p.clean('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

#print p.tokenize('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

#print p.parse('Preprocessor is #awesome 👍 https://github.com/s/preprocessor').hashtags

#l=p.parse('Preprocessor is #awesome 👍 https://github.com/s/preprocessor').hashtags

#print l[0].match
