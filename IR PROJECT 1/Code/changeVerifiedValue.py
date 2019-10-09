#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tweepy
import json
from tweepy import OAuthHandler, AppAuthHandler
from twarc import Twarc
import emoji
import pytz
import datetime
from os import listdir
from os.path import isfile, join


# In[60]:




# get files in crawledData directory
mypath = "C:/Users/Snigdha Gupta/Documents/Python Scripts/IR Project 1/cleanedCrawledData/ChangedData"
file_names = [files for files in listdir(mypath) if isfile(join(mypath,files))]

for file_name in file_names[2:3]:
    with open("cleanedCrawledData/ChangedData/"+file_name,"r") as f:
        print("Opening ", file_name[:-5])
        data = json.load(f)
        count = 0
        for tweet in data:
            # check for verified true only for POI
#             if tweet.get('verified') is True and tweet.get('in_reply_to_status_id') is None:
#                 print(tweet.get('user').get('screen_name'))
            # get tweet number for each tweet
#             print("Tweet ID:", count)
            
            # print details for each tweet
#             print("ID", tweet.get('id'), "\t User", tweet.get('user').get('screen_name'), "\t Verified", tweet.get('verified'))
            if tweet.get('user').get('screen_name') != file_name[:-5] and tweet.get('verified') is True and tweet.get('in_reply_to_status_id') is not None: 
                print("Tweet ID:", count)
                print("ID", tweet.get('id'), "\t User", tweet.get('user').get('screen_name'), "\tVerified", tweet.get('verified'))
                # update value
                tweet.update({'verified':False})
                print('changed')
            count=count+1
            
    # write to a new file
    with open("cleanedCrawledData/VerifiedChangedData/"+file_name,"w") as f:
#         json.dump(data,f)
    
print("DONE!")


# In[3]:


import os


# In[11]:


mypath = "C:/Users/Snigdha Gupta/Documents/Python Scripts/IR Project 1/cleanedCrawledData/VerifiedChangedData"
file_names = [files for files in listdir(mypath) if isfile(join(mypath,files))]


# In[14]:


for i in file_names:
    with open('cleanedCrawledData/VerifiedChangedData/'+i, 'r') as f:
        test = json.load(f)
    
    print (i, '\t Length: ', len(test))


# In[15]:


for i in file_names:
    with open('cleanedCrawledData/WrongSubmit/'+i, 'r') as f:
        test = json.load(f)
    
    print (i, '\t Length: ', len(test))


# In[ ]:




