#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tweepy
import json
from tweepy import OAuthHandler, AppAuthHandler
from twarc import Twarc
import emoji
import pytz
import datetime
from os import listdir
from os.path import isfile, join

twitterKeys = {'consumer_key' : '57YoNBcWjCcqYaQ8DT1Syuwgb', 
              'consumer_secret':'5hykB2rsb3dojMkiWkvVWhs9juJPrWZYkFShG79yUKsQhdextT',
             'access_token':'884281851237367808-K6xR79CD77Lb5Iv90RXOqFNW4u5eMyZ',
             'access_secret': 'BnQmg8NG07wVQyupdPg7T2doK6sgVPvawuWdtkCy7n6fM'}

# authenticate
auth = AppAuthHandler(twitterKeys['consumer_key'],twitterKeys['consumer_secret'])

# create twitter api object
tapi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# In[6]:


# get files in crawledData directory
mypath = "C:/Users/Snigdha Gupta/Documents/Python Scripts/IR Project 1/crawledData"
file_names = [files for files in listdir(mypath) if isfile(join(mypath,files))]
# print(file_names)
# file_names.remove("PiyushGoyal.json")
# print(file_names)
list_of_poi = []
for file_name in file_names:
#     print(file_name)
    with open("crawledData/"+file_name,"r") as f:
#         print("file opened in read mode")
        data = json.load(f)
        for tweet in data[:1]:
#             print(tweet)
            list_of_poi.append([tweet.get('poi_name'),tweet.get('poi_id'),tweet.get('country')])

print(list_of_poi)

# print(list_of_poi[0][0])


# In[7]:


for i,val in enumerate(list_of_poi):
    print(i,"  ",val)


# In[5]:


# function to extract relaed information from twitter data
def parse_tweet_data(poi,tweet,reply_flag=False,retweet_flag=False):
    # Extract only relevant data from the tweet json
    data = {'poi_name': poi[0],
            'poi_id': poi[1],
            'verified': tweet.get('user').get('verified'),
            'country': poi[2],
            'replied_to_tweet_id': tweet.get('in_reply_to_status_id'),
            'replied_to_user_id': tweet.get('in_reply_to_user_id'),
            'tweet_text': tweet.get('full_text'),
            'tweet_lang': tweet.get('lang'),
            'hashtags': [h.get('text') for h in tweet.get('entities').get('hashtags')],
            'mentions': [m.get('screen_name') for m in tweet.get('entities')['user_mentions']],
            'tweet_urls': [u.get('url') for u in tweet.get('entities')['urls']],
            'tweet_date': tweet.get('created_at'),
            'tweet_loc': tweet.get('geo'),
            'retweeted': tweet.get('retweeted'),
            'replied_to_screen_name': tweet.get('in_reply_to_screen_name'),
            'tweet_emoticons':[e for e in tweet.get("full_text") if e in emoji.UNICODE_EMOJI],
            'reply_text': None
           }
    if reply_flag:
        data.update({'reply_text': tweet.get('full_text')})
        
    if retweet_flag:
        data.update({'tweet_text': tweet.get('retweeted_status').get('full_text'),
                     'reply_text': tweet.get('retweeted_status').get('full_text')})
        
        
#     # set country
#     country_list = {"usa": ["realDonaldTrump", "abc", "", "", ""], 
#                     "india": ["narendramodi", "AmitShah", "myogiadityanath", "rajnathsingh", "yadavakhilesh"],
#                     "brazil": ["jairbolsonaro", "BolsonaroSP", "Haddad_Fernando", "LulaOficial", "MarinaSilva"]}

#     for key,val in country_list.items():
#         for person in val:
#             if person == data.get("poi_name"):
#                 data.update({"country": key})
                
    # convert date to GMT
    gmt_date = datetime.datetime.strptime(data.get('tweet_date'), '%a %b %d %H:%M:%S +%f %Y')
    gmt_date = pytz.utc.localize(gmt_date)
    gmt_date = gmt_date.astimezone(pytz.timezone('GMT'))
    gmt_date = gmt_date.replace(microsecond=0, second=0, minute=0) + datetime.timedelta(hours=1)
    gmt_date = gmt_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    data.update({'tweet_date': gmt_date})
    
    
    # update media
    try:
        data.update({'media_url': [mu.get('url') for mu in tweet.get('entities').get('media')]})
    except:
        pass
    
#     if "media" in tweet.get('entities').keys():
#         data.update({'media_url': [mu.get('url') for mu in tweet.get('entities').get('media')]})
#     else:
#         data.update({'media_url':[None]})    
    # combine data and tweet data
    data.update(tweet)
    
    return data


# In[7]:


list_of_hashtags = ["akhilesh yadav"]
# 0 Amit Shah ["#AmitShah", "#Amit shah", "amit shah"]
# 1 BernieSanders ["#BernieYellsForUs", "#BernieSanders", "Bernie2020"]
# 2 BolsonaroSP ["#bolsonaroSP", "#bolsonaropresidente", "#EduardoBolsonaro", "#bolsonaronossopresidente", "eduardo bolsonaro"]
# 3 CoryBooker ["#CoryBooker", "CoryBooker", "#cory2020", "corybooker"]
# 4 Haddad_Fernando ["#HaddadPresidente", "#TeamHaddad", "Haddad_Fernando", "#Fernando Haddad"]
# 5 jairbolsonaro ["#JairBolsonaro", "#BrazilPresident", "#jair"]
# 6 Joe Biden ["#joebiden", "#JoeBidenpresident", "#biden", "#biden2020"]
# 7 KamalaHarris ["#KamalaHarris", "Kamala", "DudeGottaGo"]
# 8 LulaOficial ["#LulaLivre", "#LulaLivreja", "Luiz Inácio Lula da Silva", "#lulapresidente", "#LulaLivreJá"]
# 9 MarinaSilva ["#MarinaSilva", "#MarinaSempre", "#Provocações", "#marinapresidente18", "marinapresidente", "marina18", "Marina Silva"]
# 10 Narendra Modi ["#NarendraModi", "#MODI", "PMMOdi"]
# 11 PiyushGoyal ["#PiyushGoyal", "#PiyushHatesMaths", "#piyushgoyaloffc", "piyushgoyal"]
# 12 rajnathsingh ["#rajnathsingh", "#defenceminister", "#rajnath", "rajnath"]
# 13 realDonaldTrump ["#donaldtrump", "#trump", "realdonaldtrump"]
# 14 yadavakhilesh ["#akhileshyadav", "#akhilesh", "#akhileshyadavji", "#youngupcm", "#yadav", "#AkhileshYadavSamajwadi", "akhileshyadav"]

poi = list_of_poi[14]
print(poi)
collect_hashtags = []
for q in list_of_hashtags:
    
    print("Searching :",q)
    hashtag_tweets = []
    retweet_count = 0
    tweet_count = 0
    print("----Start----")
    print("Total Tweets:",len(hashtag_tweets))
    print("Retweets:",retweet_count)
    print("Tweets:",tweet_count)
    print("-------------")
    for i,hashtag in enumerate(tweepy.Cursor(tapi.search,q,tweet_mode='extended').items(4000)):

        retweet_flag = False

        # check if tweet
        h_retweet = hashtag._json.get('retweeted_status')
        if h_retweet:
#             retweet_flag = True
            if retweet_count < 300:
                if hashtag._json.get('in_reply_to_status_id'):
                    hashtag_tweets.extend([parse_tweet_data(poi,hashtag._json,reply_flag=True,retweet_flag=True)])
                else:
                    hashtag_tweets.extend([parse_tweet_data(poi,hashtag._json,reply_flag=False,retweet_flag=True)])
                retweet_count =retweet_count + 1
            else:
                continue
        elif hashtag._json.get('in_reply_to_status_id') and hashtag._json.get('in_reply_to_user_id') != poi[2]:
            tweet_count = tweet_count + 1
            hashtag_tweets.extend([parse_tweet_data(poi,hashtag._json,reply_flag=True)])
        elif hashtag._json.get('user').get('screen_name') != poi[0]:
            tweet_count = tweet_count + 1
            hashtag_tweets.extend([parse_tweet_data(poi,hashtag._json,reply_flag=False)])


        if i%100 == 0:
            print("Total Tweets:",len(hashtag_tweets))
            print("Retweets:",retweet_count)
            print("Tweets:",tweet_count)
        if i>800:
            break
    print("Collecting hashtags")
    collect_hashtags.extend(hashtag_tweets)
    print("TOTAL ",poi[0], "hashtags \t",len(collect_hashtags))
    if len(collect_hashtags) > 1500:
        print('1500 hashtagged tweets collected')
        break
    print("---------------------------------------------")
        
# print(retweet_count)
# print(len(hashtag_tweets))


# In[8]:


len(collect_hashtags)


# In[9]:


x = []
x.extend(collect_hashtags)
print(len(x))


# In[10]:


with open("crawledData/HashtagsCrawls/hashtags_"+poi[0]+"2.json","w") as f:
    json.dump(x,f)
print("Done!")


# In[64]:


x = "this, is a test 'string' to remove punctuations and it's pretty damn hard!"
x=x[:-1]
print(x)


# In[97]:


list_of_poi[11]


# In[ ]:




