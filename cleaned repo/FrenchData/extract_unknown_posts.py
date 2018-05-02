import glob

import pandas as pd

pd.options.display.max_rows = 30

data_folder = r'./Accounts/q1_output/*.csv'
output_loc = r'allpostswithunknown.csv'

CSV_COLUMNS = ['caption_original', 'category', 'account_name']


### To be updated later to save to file
pd.options.display.max_rows = 1000
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)

data_df = pd.DataFrame()
print(filePaths)
for f in filePaths:
    print(f)
    df = pd.read_csv(f, encoding='utf-8')
    if df.shape[0] < 1:
        continue
    df = df[CSV_COLUMNS]
    data_df = pd.concat([data_df, df])
data_df = data_df.loc[data_df['category'] == 'unknown']
data_df.to_csv(output_loc, index=CSV_COLUMNS)

#get number of unknowns by account_name
result = data_df.groupby(['account_name']).size()
print(result)
