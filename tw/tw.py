import tweepy
import inspect
import csv
import ftfy

# Fill the X's with the credentials obtained by 
# following the above mentioned procedure.
consumer_key='dukNsGvrvbsqOje2G9F1e8AjJ'
consumer_secret='4GdC8KyqeppsYnqzFDUEXuEb2O233uAQWLhmfz4lNdaYNEUMeP'
access_key='951575833310765056-LAOyHYshSF2OLB5uQ2ApjVhbrUy8gMV'
access_secret='L7AKlZnULumHSb0TE88VTcyLyMctwKFXIGxDMpX6u32zX'
# Driver code
if __name__ == '__main__':
 
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    #get_tweets("ParksCanada") 
    
    usernames = ['ParcsCanada','ParksCanada','environmentca','environnementca','ec_minister','ministre_ec','NRCan','RNCan','ENERGYSTAR_CAN','Transport_gc','Transports_gc','CTA_gc','OTC_gc','TSBCanada','BSTCanada','AAFC_Canada','AAC_Canada','CCG_GCC','GCC_CCG','DFO_CCG_Quebec','MPO_GCC_Quebec','DFO_Central','MPO_Centre','DFO_Gulf','MPO_Golfe','DFO_MAR','MPO_MAR','DFO_MPO','MPO_DFO','DFO_NL','MPO_TNL','DFO_Pacific','MPO_Pacifique','DFO_Science','MPO_Science','AskISED','DemandezaISDE','GCIndigenous','GCAutochtones','GiantMine','MineGiant']
    #usernames = ['MPO_Science','AskISED','DemandezaISDE','GCIndigenous','GCAutochtones','GiantMine','MineGiant']
        
    for username in usernames:
    # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # Access to user's access key and access secret
        auth.set_access_token(access_key, access_secret)

        # Calling api
        api = tweepy.API(auth,retry_count=5,
                     retry_delay=10,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
        tweets=[]


        year=2018
    
        print (api.rate_limit_status()['resources']['statuses']['/statuses/user_timeline'])
   
        with open('%s_tweets.csv' % username, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["id","full_text","retweet_count","favorite_count","created_at"])
            for status in tweepy.Cursor(api.user_timeline,screen_name=username, tweet_mode="extended",exclude_replies = True, exclude_retweets =True ).items(50000):
                if year<=2015:
                    break


                year = int(status.created_at.year)

                print (status.id)
                print (status.full_text)
                print (status.retweet_count)
                print (status.favorite_count)
                print (status.created_at)

                writer.writerow([status.id,
                                       ftfy.fix_encoding(status.full_text),
                                       status.retweet_count,
                                       status.favorite_count,
                                       status.created_at])
    
    
    