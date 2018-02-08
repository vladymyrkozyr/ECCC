- Parsed the data and extracted the hashtags included in either the posts/tweets or in the comments and saved them in a separate column under the name "hashtags" in each account file for Facebook, Instagram and Twitter.
- We also, extracted the urls included in the posts/tweets and saved them in a separate column called "urls". Also, for all social media accounts.
- Also, when it exists, we removed the "\n\n" that appears - it was automatically generated after we converted the files format to .csv during the data extraction phase- in the text in the posts/tweets.
- We used the following API: tweet-preprocessor in Python
- Preprocessed data, cleaned from hashtags and links is located at '(social network name)/cleaned data/'


_________________________________________________________

STEP 2 Cleaning resulst are located in '(social network name)/filtered_data/'
