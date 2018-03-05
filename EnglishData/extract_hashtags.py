import glob
import os
import pandas as pd
import itertools
import operator
import numpy as np
data_folder = './Accounts/*.csv'

outputDir = os.path.dirname(data_folder) + '/output/'

filePaths = glob.glob(data_folder)  
hashtags=[]
for filename in filePaths:
    print(filename)
    basename = os.path.basename(filename)
    outputFileName = outputDir + basename
    data_df = pd.read_csv(filename, encoding='utf-8')
    
    for i, hashtag_list in data_df.iterrows():
    #for hashtag_list in data_df['hashtags']:
        #for h in hashtag_list['hashtags']:
        hashtags.append(hashtag_list['hashtags'])
        #print hashtags
        
#hashtags = reduce(operator.add, hashtags)

print hashtags

l=`hashtags`.replace('[', '').replace(']', '').replace('"','').replace("'",'').replace(' ','').split(',')



l=sorted(list(set(l)))
print l 

k=pd.DataFrame({'hashtags':l})
    
k.to_csv('hashtags.csv',index=None)
#    
#    output_df = data_df[output_list]
#    output_df.to_csv(outputFileName, index=None)   
