#!/usr/bin/env python
# coding: utf-8

# In[10]:


import json
import datetime
from os import listdir
from os.path import isfile, join

mypath = "C:/Users/Snigdha Gupta/Documents/Python Scripts/IR Project 1/cleanedCrawledData"
file_names = [files for files in listdir(mypath) if isfile(join(mypath,files))]

for file in file_names:
    print(file)
    with open("cleanedCrawledData/"+file, "r") as f:
        data = json.load(f)

    count = 0

    for tweet in data:
        if tweet.get('retweeted_status'):
            count=count+1

    print(count)


# In[ ]:




