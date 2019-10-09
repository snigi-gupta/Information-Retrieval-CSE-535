#!/usr/bin/env python
# coding: utf-8

# In[7]:


import tweepy
import json
from tweepy import OAuthHandler, AppAuthHandler
from twarc import Twarc
import emoji
import pytz
import datetime


# In[8]:


twitterKeys = {'consumer_key' : '57YoNBcWjCcqYaQ8DT1Syuwgb', 
              'consumer_secret':'5hykB2rsb3dojMkiWkvVWhs9juJPrWZYkFShG79yUKsQhdextT',
             'access_token':'884281851237367808-K6xR79CD77Lb5Iv90RXOqFNW4u5eMyZ',
             'access_secret': 'BnQmg8NG07wVQyupdPg7T2doK6sgVPvawuWdtkCy7n6fM'}

# authenticate
auth = AppAuthHandler(twitterKeys['consumer_key'],twitterKeys['consumer_secret'])


# In[9]:


# create twarc objec
tObj = Twarc(twitterKeys['consumer_key'],twitterKeys['consumer_secret'],twitterKeys['access_token'],twitterKeys['access_secret'])

# create twitter api object
tapi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# In[37]:


# function to extract relaed information from twitter data
def parse_tweet_data(tweet,reply_flag=False):
    # Extract only relevant data from the tweet json
    data = {'poi_name': tweet.get('user').get('screen_name'),
            'poi_id': tweet.get('user').get('id'),
            'verified': tweet.get('user').get('verified'),
            'country': tweet.get('user').get('location'),
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
        data.update({'poi_name': tweet.get('in_reply_to_screen_name'),
                     'poi_id': tweet.get('in_reply_to_user_id'),
                     'reply_text':tweet.get('full_text'),
                    })
    # set country
    country_list = {"usa": ["realDonaldTrump", "KamalaHarris", "BernieSanders", "CoryBooker", "JoeBiden"], 
                    "india": ["narendramodi", "AmitShah", "PiyushGoyal", "rajnathsingh", "yadavakhilesh"],
                    "brazil": ["jairbolsonaro", "BolsonaroSP", "Haddad_Fernando", "LulaOficial", "dilmabr", "rodrigobocardi"]}

    for key,val in country_list.items():
        for person in val:
            if person == data.get("poi_name"):
                data.update({"country": key})
                
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


# In[24]:


# function to search replies using tweepy
def search_replies(twitter_user,since_id,max_id,tweet):
    #print("twitterUser:", twitter_user, "sinceID:", since_id, 'max_id:', max_id)
    tweet_replies = []
#     dummy_value = 20000000
#     multiplier = 1
    i =0
    for reply in tweepy.Cursor(tapi.search,twitter_user,since_id=since_id,max_id=max_id, tweet_mode='extended').items(3000):
        i = i+1
        # get the in_reply_to_status_id
        verified_id = reply._json.get('in_reply_to_status_id')       
        
        if len(tweet_replies) < 21:
            if since_id == verified_id:
                tweet_replies.extend([parse_tweet_data(reply._json,reply_flag=True)])
        else:
            break
#     print("sinceID: ",since_id,"\t\t maxID: ", max_id)
    print("loopCount: ", i, "\t replyCount: ",len(tweet_replies), '\n')
    
#     if len(tweet_replies) < 21:
#         if max_id is None:
#             max_id = reply._json.get('id')
#         max_id = max_id + dummy_value * multiplier
#         multiplier = multiplier * 2    
#         search_replies(twitter_user,since_id,max_id,tweet)
    
    return tweet_replies


# In[40]:


counter = 0
last_tweet_id = False
twitter_user = 'LulaOficial'
tweet_list = []
max_id = None
tweet_count = 0

while counter < 11:
    
    if last_tweet_id:
        tw = tapi.user_timeline(twitter_user, count=200, include_rts=True, tweet_mode='extended', max_id = max_id)
        
    else:
        last_tweet_id = True
        tw = tapi.user_timeline(twitter_user, count=200, include_rts=True, tweet_mode='extended')

    for tweet in tw:
        tweet_count = tweet_count + 1
        current_tweet_id = tweet._json.get("id")
        dummy_value = 20000000000
        multiplier = 1
        tweet_date_limit = (datetime.datetime.today() - tweet.created_at).days
        print("Tweet:", tweet_count,"\t ID: ", current_tweet_id,"\n")
        if tweet_date_limit < 7:
            tweet_replies = []
            #temp_list = []
            #tweet_replies = [parse_tweet_data(tweet._json)]
            # call function to search replies.
            #tweet_replies.extend(search_replies("to:{}".format(twitter_user) + " filter:replies", current_tweet_id,max_id,tweet))
            while len(tweet_replies) < 24 and multiplier < 35:
                #if max_id is None:
                #    max_id = tweet_replies[len(tweet_replies)-1].get('tweet_id')
                # call function to search replies.
                tweet_replies.extend(search_replies("to:{}".format(twitter_user) + " filter:replies", current_tweet_id,max_id,tweet))

                if len(tweet_replies) < 21:
                    max_id = max_id + dummy_value * multiplier
                    multiplier = multiplier * 2
                    print("Continue Search for replies with: ", multiplier, " multiplier")
                else:
                    break
                #temp_list = (search_replies(twitter_user,current_tweet_id,max_id,tweet))
                #if len(temp_list) > 21:
                #    tweet_replies.extend(temp_list)
            print("----------------------------------------------------------")
            if len(tweet_replies)>=20 and len(tweet_replies)<24:
                tweet_list.extend([parse_tweet_data(tweet._json)])
                tweet_list.extend(tweet_replies)
                print("Saved!")
        
            #for reply in tObj.replies(tweet._json):
            #if len(tweet_replies) > 20:
            #    tweet_list.extend(tweet_replies)
            #    break
            #else:
            #    tweet_replies.extend([parse_tweet_data(reply)])
            #    replyCount = replyCount + 1

            #print("Tweet ID: ", counter, "\t\t Total Replies:", replyCount)
        else:
#             tweet_list.extend([parse_tweet_data(tweet._json)])
            break
        max_id = current_tweet_id
        
        with open("crawledData/5DayCrawls/{}".format(twitter_user)+"5.json","w") as f:
            json.dump(tweet_list,f)
    counter = counter + 1


# In[ ]:


len(tweet_list)
len(tweet_replies)

i=0
for c in tweet_list:
    try:
        if not c.get('replied_to_tweet_id'):
            i = i + 1
    except Exception as e:
        print (e, '\n', c)
print(i)


# In[55]:


tweet_list[1]


# In[18]:


tweet_list[16]


# In[14]:


storedTweet = tapi.user_timeline("TheWeirdWorld", count=100, include_rts=True, tweet_mode='extended')

data = storedTweet[15]._json
tweet_id = data.get('id')
previous_tweet_id = storedTweet[14]._json.get('id')
print(previous_tweet_id)

start_date = datetime.datetime.strptime(data.get('created_at'), "%a %b %d %H:%M:%S +%f %Y")
print("start_date: ", start_date, "\t tweet_id: ",tweet_id, '\n text: ', data.get('full_text'))
until = start_date + datetime.timedelta(days=1)
until = datetime.datetime.strftime(until, "%Y-%m-%d")

# datetime.datetime.strftime(until, "%Y-%m-%d")
temp = []
for i in tapi.search(q='@TheWeirdWorld filter:replies',since_id = data.get('id'), count=1000):
    check = i._json.get('created_at')
    print(i._json)
#     print(tweet_id == i._json.get('in_reply_to_status_id'))
    
    if (i._json.get('in_reply_to_status_id') == None):
        print (i._json)
        temp1 = i._json
        break
    if tweet_id == i._json.get('in_reply_to_status_id'):
        temp.extend([i._json])
        
#         print(temp.extend([i._json]))
#     check = datetime.datetime.strptime(data.get('created_at'), "%a %b %d %H:%M:%S +%f %Y")
#     check = datetime.datetime.strftime(check, "%Y-%m-%d")


# In[ ]:


var = "yes"
print("to:{}".format(var)+"NO")


# In[13]:


temp1


# In[ ]:




