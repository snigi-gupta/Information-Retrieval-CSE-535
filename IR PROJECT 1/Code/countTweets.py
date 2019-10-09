#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

twitter_user = "hashtags_yadavakhilesh2"
with open("cleanedCrawledData/"+twitter_user+".json", "r") as f:
    data = json.load(f)

en_count=0
hi_count=0
pt_count=0

tweets=0
replies=0
total=0

# len(tweet_list)
# len(tweet_replies)



for tweet in data:
    total = total + 1
    try:
        if tweet.get('text_en') != None:
            en_count = en_count + 1
        if tweet.get('text_hi') != None:
            hi_count = hi_count + 1
        if tweet.get('text_pt') != None:
            pt_count = pt_count + 1
            
        
        if not tweet.get('replied_to_tweet_id'):
            tweets = tweets + 1
        else:
            replies = replies + 1
        
    except Exception as e:
        print("EXCEPTION", e, '\n', tweet)
        
print("en_count : ", en_count)
print("hi_count : ", hi_count)
print("pt_count : ", pt_count)
print("tweets : ", tweets)
print("replies : ", replies)
print("total : ", total)
# # i=0
# for c in tweet_list:
#     try:
#         if not c.get('replied_to_tweet_id'):
#             i = i + 1
#     except Exception as e:
#         print (e, '\n', c)
# print(i)


# In[ ]:




