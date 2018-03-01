- Parsed the data and extracted the hashtags included in either the posts/tweets or in the comments and saved them in a separate column under the name "hashtags" in each account file for Facebook, Instagram and Twitter.
- We also, extracted the urls included in the posts/tweets and saved them in a separate column called "urls". Also, for all social media accounts.
- Also, when it exists, we removed the "\n\n" that appears - it was automatically generated after we converted the files format to .csv during the data extraction phase- in the text in the posts/tweets.
- We used the following API: tweet-preprocessor in Python
- Preprocessed data, cleaned from hashtags and links is located at '(social network name)/cleaned data/'


_________________________________________________________

STEP 2 Cleaning resulst are located in '(social network name)/filtered_data/'


---------------------MARCH 1 UPDATE------------------------------

- Q1: 
- — sentiment column is formed according to average sentiment for all comments of the post
- — posts are sorted descending by Reactions_sum column
- — each post is categorized to one of three categories according to keyword list 
- — also word_matched_list contains keywords which post contains
- — added column account_name in case if files need to be merged

- Q2:
- — extracted top 5 post for each month per account and merged them into merged file
- — unmerged files are in merging folder

- Q3 and Q4:
- — assigned FSDS goal for each post in FSDS_Goal_Category
- — also FSDS_Goal_Category_word_list contains keywords of 13 FSDS goals which post contains