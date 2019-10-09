#!/usr/bin/env python
# coding: utf-8

# In[7]:


import json
import datetime

twitter_user = "MarinaSilva5"
with open("cleanedCrawledData/"+twitter_user+".json", "r") as f:
    data = json.load(f)

reply_count = 0

one_days_ago = datetime.datetime.today()
five_days_ago = datetime.datetime.today() - datetime.timedelta(days=9)
tweet_ids = []

for tweet in data:
    if five_days_ago <= datetime.datetime.strptime(tweet.get('created_at'),'%a %b %d %H:%M:%S +%f %Y') <= one_days_ago:
        if tweet.get('replied_to_tweet_id') is None:
            tweet_ids.append([tweet.get('id'),tweet.get('created_at')])
        
print(tweet_ids)

for t_ids in tweet_ids:
    count = 0
    for tweet in data:
        if tweet.get('in_reply_to_status_id') is not None and tweet.get('in_reply_to_status_id') == t_ids[0]:
            count = count + 1
    print("Reply Count for tweet ID:",t_ids, "= ",count)


# In[81]:


x = datetime.datetime.today() - datetime.timedelta(days=7) - datetime.datetime.strptime(data[0].get('created_at'), '%a %b %d %H:%M:%S +%f %Y')


# In[20]:


t = datetime.datetime.today() - datetime.timedelta(days=7)


# In[21]:


t


# In[ ]:




