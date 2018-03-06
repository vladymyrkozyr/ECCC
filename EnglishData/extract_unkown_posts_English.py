import glob

import pandas as pd


pd.options.display.max_rows = 30

data_folder = 'Accounts/output_chelsea/*.csv'

CSV_COLUMNS = ['caption_original', 'category', 'account_name']


### To be updated later to save to file
pd.options.display.max_rows = 1000
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)
data_df = pd.DataFrame()
for f in filePaths:
    print(f)
    df = pd.read_csv(f, encoding='utf-8')
    if df.shape[0] < 1:
        continue
    df = df[CSV_COLUMNS]
    data_df = pd.concat([data_df, df])
data_df = data_df.loc[data_df['category'] == 'unknown']
data_df.to_csv('allpostswithUnknown_English.csv', index=CSV_COLUMNS)
