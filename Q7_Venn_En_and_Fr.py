
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


en_file = './EnglishData/Accounts/q7_output/q1_not_other_classes_en.csv'
fr_file = './FrenchData/Accounts/q7_output/q1_not_other_classes_fr.csv'


# In[3]:


pd.options.display.max_rows = 10
# read csv files and save targt columns to dataframe
df_en = pd.read_csv(en_file, encoding = 'utf-8')
df_fr = pd.read_csv(fr_file, encoding = 'utf-8')
df = df_en.append(df_fr, ignore_index=True)
df


# # Plot Venn Diagram

# In[4]:


econ = set(df[df['Economical'] == 1].id)
env = set(df[df['Environmental'] == 1].id)
soc = set(df[df['Social'] == 1].id)


# In[5]:


plt.clf()
plt.figure(figsize=(10,10))
rcParams['font.size'] = 13
venn3([econ, env, soc], ('Economical', 'Environmental', 'Social'))
plt.savefig('./q7_venn_diagram_en_and_fr.png')
plt.show()

