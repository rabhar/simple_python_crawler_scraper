
# coding: utf-8

# In[150]:


import requests
from lxml import etree, html
import time
import random
import pandas as pd
import numpy as np


# In[151]:


#crawling as alexa bot
headers = {'User-Agent': 'Mozilla/5.0 (compatible; ia_archiver/1.0; +http://www.alexa.com/help/webmasters; crawler@alexa.com)'}


# In[152]:


#initializing variables
#crawl pages
area_urls = []
row = []
failed_urls = []
next_url = ""


# In[153]:


res = requests.get('https://www.zomato.com/chennai',headers=headers)
tree = html.fromstring(res.content)


# In[154]:


#get all areas inside chennai
area_urls = tree.xpath("//section[contains(./h2,'Popular localities')]//a/@href")


# In[155]:


for area in area_urls[0:1]:
    # hardcoding all=1 parameter to show all restaurants
    res = requests.get( area + '?all=1',headers=headers)
    tree = html.fromstring(res.content)
    #loop to scrape restaurant name, price, etcs from all the pages
    while True:
        try:
            for restaurant in tree.xpath("//div[contains(@class,'search-card')]"):
                title = restaurant.xpath(".//a[@data-result-type='ResCard_Name']/text()")[0].strip() if(len(restaurant.xpath(".//a[@data-result-type='ResCard_Name']/text()"))) else np.nan
                location = restaurant.xpath(".//a[contains(@class,'search_result_subzone')]/b/text()")[0].strip() if(len(restaurant.xpath(".//a[contains(@class,'search_result_subzone')]/b/text()"))) else np.nan
                costForTwo = restaurant.xpath(".//div[contains(@class,'search-page-text')]//span[contains(.,'Cost for two')]//following-sibling::span/text()")[0].strip() if(len(restaurant.xpath(".//div[contains(@class,'search-page-text')]//span[contains(.,'Cost for two')]//following-sibling::span/text()"))) else np.nan
                cuisine = ','.join((restaurant.xpath(".//div[contains(@class,'search-page-text')]//span[contains(.,'Cuisine')]//following-sibling::span/a/text()"))) if(len(restaurant.xpath(".//div[contains(@class,'search-page-text')]//span[contains(.,'Cuisine')]//following-sibling::span/a/text()"))) else np.nan
                ratings = restaurant.xpath(".//div[contains(@class,'rating-popup')]/text()")[0].strip() if(len(restaurant.xpath(".//div[contains(@class,'rating-popup')]/text()"))) else np.nan
                review_counts = restaurant.xpath(".//span[contains(@class,'rating-votes')]/text()")[0].strip() if(len(restaurant.xpath(".//span[contains(@class,'rating-votes')]/text()"))) else np.nan
                phone = restaurant.xpath(".//div[contains(@class,'search-result-action')]//a[contains(@class,'ph-info')]/@data-phone-no-str")[0].strip()
                url = restaurant.xpath(".//a[@data-result-type='ResCard_Name']/@href")[0].strip() if(len(restaurant.xpath(".//div[contains(@class,'search-result-action')]//a[contains(@class,'ph-info')]/@data-phone-no-str"))) else np.nan
                
                #storing attributes in a atuple for pandas dataframe
                row.append((title,location,costForTwo,cuisine,ratings,review_counts,phone,url))

            next_url = tree.xpath("//a[contains(@class,'next')]/@href")
            if(len(next_url)):
                print(next_url[0])
                # looping through all pages
                res = requests.get( "https://www.zomato.com" + next_url[0] ,headers=headers)
                tree = html.fromstring(res.content)
            else:
                break
        except Exception as e:
            print(e)
            failed_urls.append(next_url)    

df = pd.DataFrame(row,columns=['title', 'location', 'cost_for_two', 'cuisine','ratings','review_counts','phone','url'])
df.to_csv("zomato_restaurants_in_chennai.csv")
with open("failed_urls.txt", 'w+', encoding='utf-8') as r:
        r.write("\n".join(failed_urls))

