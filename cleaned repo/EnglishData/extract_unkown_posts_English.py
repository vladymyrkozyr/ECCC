import glob

import pandas as pd


pd.options.display.max_rows = 30

data_folder = 'Accounts/q1_output/*.csv'

CSV_COLUMNS = ['caption_original', 'category', 'account_name']


### To be updated later to save to file
pd.options.display.max_rows = 1000
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)
data_df = pd.DataFrame()
x=0
for f in filePaths:
    print(f)
    df = pd.read_csv(f, encoding='utf-8')
#    
#    if df.shape[0] < 1:
#        continue
    cap=[]
    cat=[]
    acc=[]
    for i, p in df.iterrows():
        x+=1
        if p['category']=='unknown' and len(str(p['caption_original']))!=0:
            cap.append(p['caption_original'])
            cat.append(p['category'])
            acc.append(p['account_name'])
            
            
    k=pd.DataFrame({'category':cat,'caption_original':cap,'account_name':acc})
    
    #df = df[CSV_COLUMNS]
    data_df = pd.concat([data_df, k])
#data_df = data_df.loc[data_df['category'] == 'unknown']
data_df.to_csv('allpostswithUnknown_English.csv')

result = data_df.groupby(['account_name']).size()
print(result)
print()
print("Total unknowns: {}".format(len(data_df)))
print("Total posts: {}".format(x))
