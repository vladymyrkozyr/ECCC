
# coding: utf-8

# In[76]:


import pandas as pd
import glob, os

from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer


# In[91]:


def getSentiment(row):
    text = str(row['text_original'])
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    return blob.sentiment[0]

def discretizeSentiment(row):
    result = ''
    if row['text_sentiment_original_scores'] < 0:
        result = 'negative'
    if row['text_sentiment_original_scores'] == 0:
        result = 'neutral'
    if row['text_sentiment_original_scores'] > 0:
        result = 'positive'
    if result == '':
        print ('Alert!')
    return result


def discretizeSentiment2(row):
    result = ''
    if row['average_sentiment_score'] < 0:
        result = 'negative'
    if row['average_sentiment_score'] == 0:
        result = 'neutral'
    if row['average_sentiment_score'] > 0:
        result = 'positive'
    if result == '':
        print ('Alert!')
    return result



# In[104]:


def getAvgSentiment(row):
    result = 0
    if 'id' in row.index:
        id = row['id']
    else:
        id = row['status_id']
        
    if id in groupedDF.index:
        result = groupedDF[id]
    
    return result
    


# In[119]:


commentsPath = r'./Accounts/Comments/'
postsPath = r'./Accounts/'

comments_files = glob.glob(commentsPath+"*.csv")


for comment_file in comments_files:
    
    name = os.path.basename(comment_file)
    print(name)
     
    commentsDF = pd.read_csv(comment_file, encoding='utf-8').drop(['text_sentiment_original_scores', 'text_sentiment_original_scores_type'], axis=1)
        
    commentsDF['text_sentiment_original_scores'] = commentsDF.apply(getSentiment, axis=1)
    commentsDF['text_sentiment_original_scores_type'] = commentsDF.apply(discretizeSentiment, axis=1)
    
    # save to csv file
    commentsDF.to_csv(commentsPath+name, encoding='utf-8', index=False)
    
    # do a groupby to get mean sentiment of comments per post so groupby 'post_id' for in, 'status_id' for fb
    if 'facebook' in name:
        groupedDF = commentsDF.groupby('status_id')['text_sentiment_original_scores'].mean()
    else:
        groupedDF = commentsDF.groupby('post_id')['text_sentiment_original_scores'].mean()
    
    # now we have the average comment sentiment for each post and I want to put it into the posts 

    # construct the name of the corresponding post/status file
    if 'facebook' in name:
        post_file = name.replace('comments', 'statuses')
    else:
        post_file = name.replace('comments', 'posts')
        
    print(comment_file+"<======>"+post_file)
        
    # read in the posts file and drop the old incorrects columns
    postsDF = pd.read_csv(postsPath+post_file, encoding='utf-8')
    if 'average_sentiment_score' in postsDF.columns:
        postsDF = postsDF.drop('average_sentiment_score', axis=1)
    if 'words_matched_list' in postsDF.columns:
        postsDF = postsDF.drop('words_matched_list', axis=1)
    if 'sentiment' in postsDF.columns:
        postsDF = postsDF.drop('sentiment', axis=1)
    if 'category' in postsDF.columns:
        postsDF = postsDF.drop('category', axis=1)
    
    # now I have the posts file in a DF and I need to go through each row, 
    # look up the post/status_id in the groupedDF above and get the average sentiment and put it in a column
    postsDF['average_sentiment_score'] = postsDF.apply(getAvgSentiment, axis=1)
    postsDF['sentiment'] = postsDF.apply(discretizeSentiment2, axis=1)
 
   
    # save to csv file
    postsDF.to_csv(postsPath+post_file, encoding='utf-8', index=False)






    

