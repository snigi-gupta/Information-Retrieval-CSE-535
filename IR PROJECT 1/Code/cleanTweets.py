#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import re


twitter_user = "AmitShah"
# jairbolsonaro for e 10 - 13
# narendramodi for # and @ and url 0-3

with open("crawledData/"+twitter_user+".json", "r") as f:
    data = json.load(f)

# slice data
# s = slice(0,1)
# data = data[s]

i=0
# get stopwords

for tweet in data:
    i=i+1
    fillers = []
    mu=0
    temp_text = tweet.get('tweet_text')
    fillers.extend(["#"+h for h in tweet.get('hashtags')])
    fillers.extend(["@"+m for m in tweet.get('mentions')])
    fillers.extend([u for u in tweet.get('tweet_urls')])
    fillers.extend(tweet.get('tweet_emoticons'))
    try:
        fillers.extend([mu for mu in tweet.get('media_url')])
    except Exception as e:
        pass
#     print(fillers)
    
    for filler in fillers:
#         print("filler",filler)
#         print("temp_text:\n",temp_text)
#         print("----------------------")
        temp_text = re.sub(filler,'',temp_text)
#         print(temp_text)
#         print("new_text:\n",temp_text)
#         print("----------------------")
    
    if tweet.get('tweet_lang') == "en":
        tweet.update({"text_en":temp_text})

    if tweet.get('tweet_lang') == "hi":
        tweet.update({"text_hi":temp_text})

    if tweet.get('tweet_lang') == "pt":
        tweet.update({"text_pt":temp_text})
        
#     break
#     print(tweet.get('poi_name'),"TweetID ",i)
#     print("-------------------")
#     print(tweet.get('tweet_text'))
#     print("-------------------")
#     print(tweet.get('text_en'))
#     print(tweet.get('text_hi'))
#     print(tweet.get('text_pt'))
    
#     print("*******************")
    
with open("cleanedCrawledData/"+twitter_user+".json","w") as f:
    json.dump(data,f)

print("DONE!") 


# In[14]:


# clean tweets: set country
import json
with open("crawledData/HillaryClinton.json","r") as f:
    data = json.load(f)

for d in data:
    d.update({'country': "usa"})

with open("crawledData/HillaryClinton1.json","w") as f:
    json.dump(data,f)
print('Done')


# In[115]:


# clean tweets: add key
import json

twitter_user = "AmitShah"
with open("crawledData/"+twitter_user+".json","r") as f:
    data = json.load(f)
i=0
for d in data:
    i=i+1
    if d.get('in_reply_to_status_id'):
#         print(d.get('in_reply_to_status_id'))
        d.update({'reply_text':d.get('tweet_text')})
    else:
        d.update({'reply_text':None})
#         print(d)
print(i,"changes made")
with open("crawledData/"+twitter_user+"1.json","w") as f:
    json.dump(data,f)
print('Done')


# In[32]:


data


# In[ ]:


d


# In[ ]:




