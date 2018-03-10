
# coding: utf-8

# In[1]:


import glob
import os
import sys
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from pylab import *
import seaborn as sns
sns.set()

pd.options.display.max_rows = 30


# In[2]:


keywords_chosen = 'Keywords_ECCC_EN.csv'

data_folder = './Accounts/q1_output/*.csv'

OUTPUT_COLS = ['id','date_published','link','caption_original','caption_cleaned','hashtags','num_comments',
               'num_shares','num_likes','Reactions_SUM','matched_keywords','language',
               'average_sentiment_score','sentiment','category',]


# In[3]:


# create output directory
outputDir = os.path.dirname(data_folder).replace('q1_output', 'q7_output') + '/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


# In[4]:


pd.options.display.max_rows = 10
# read csv files and save targt columns to dataframe
filePaths = glob.glob(data_folder)  
data_df = pd.DataFrame(columns=OUTPUT_COLS)
for filename in filePaths:
    print(filename)    
    df_i = pd.read_csv(filename, encoding = 'utf-8')
    data_df = data_df.append(df_i, ignore_index=True)


# In[5]:


df = data_df[['id', 'date_published','caption_original','matched_keywords','category']]
df = df[~df['category'].str.contains('other')]


# In[6]:


col_list = ['Economical', 'Environmental', 'Social']
for col in col_list:
    df[col] = 0
    df.loc[df.category.str.contains(col), col] = 1
df.to_csv(outputDir + 'q1_not_other_classes_en.csv', index=None, encoding='utf-8')
df


# # Plot Venn Diagram

# In[7]:


econ = set(df[df['Economical'] == 1].id)
env = set(df[df['Environmental'] == 1].id)
soc = set(df[df['Social'] == 1].id)


# In[8]:


plt.clf()
plt.figure(figsize=(10,10))
rcParams['font.size'] = 13
venn3([econ, env, soc], ('Economical', 'Environmental', 'Social'))
plt.savefig(outputDir + 'q7_venn_diagram_en.png')
plt.show()

