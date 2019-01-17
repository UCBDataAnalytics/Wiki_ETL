
# coding: utf-8

# In[48]:


import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
import pymongo


# In[49]:


conn = 'mongodb://root:ucbmongodb@35.184.4.63:27017'
client = pymongo.MongoClient(conn)
db = client.wikidb


# In[50]:


file = pd.read_table("/Users/teresalee/Desktop/Wiki_ETL/wiki_short.txt")
# url='wikihgdshk?title='


# In[53]:


for title in file['Page Title'].values[0:212]:
    url = 'https://en.wikipedia.org/wiki/'+ title
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    category = soup.find("div", "mw-normal-catlinks")
    category2= category.find_all('li')
    cat = [temp_cat.text for temp_cat in category2]
    cat_length = len(cat)
    
    cat_list = {
        "TITLE":title,
        "URL": url,
        "CATEGORIES":cat,
        "NUM OF CATEGORIES": cat_length
    }
    print(cat_list)
    
    db.categories.insert_one(cat_list)
