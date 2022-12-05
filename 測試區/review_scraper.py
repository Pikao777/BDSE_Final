#!/usr/bin/env python
# coding: utf-8

# # Python3.9.12

# ## 使用套件

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import requests
import sys
import os
import time
import json
import html2text
import pandas as pd
import undetected_chromedriver as uc
from datetime import datetime
import json
from webdriver_manager.chrome import ChromeDriverManager


# ## 店家詳細資訊+評論

# In[3]:


def initialize_chrome(_from="facebook",retry=0):
    global driver 
    try:
        print("Initializing chromedriver.")
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        time.sleep(2)
        return True
    except Exception as e:
        print(e)
        pass

def parse_description(description_tag):
    h = html2text.HTML2Text()
    h.ignore_links = True
    description_text = h.handle(str(description_tag)) 
    return description_text

#review區域
def get_review():
    print('請輸入開始數字\n')
    num = int(input())
    end_num = 22882
    while num <= end_num:
        # 下一頁review內容的token(寫進url)
        next_page_token = ""

        # 設定biz_id(寫進url)
        url = df['google_url'][num]
        biz_id = re.search(r"1s(0.*?\:.*?)[^a-zA-Z\d\s:]", url) # 寫成迴圈的時候要改一下
        if not biz_id:
            print("Not a valid url.")
        biz_id = biz_id.groups()[0]
        place_name = df['place_name'][num]
        file_name = df['file_name_2'][num]
        reviewData = []
        try:
            while True:
                url = f'https://www.google.com/async/reviewSort?yv=3&async=feature_id:{biz_id},review_source:All%20reviews,sort_by:newestFirst,is_owner:false,filter_text:,associated_topic:,next_page_token:{next_page_token},_pms:s,_fmt:json'
                response = requests.get(url)

                response = response.text.removeprefix(")]}'")

                json_data = json.loads(response)["localReviewsProto"]

                if json_data.get('other_user_review'):
                    review_data = json_data["other_user_review"]

                    for result in review_data:
                        personal_rating = result['star_rating']['value']
                        author_name = result['author_real_name']
                        review_date = result['publish_date']['localized_date']
                        review_acquisition_date = datetime.now().strftime("%Y-%m-%d")
                        if result.get('review_text'):
                            review_text = parse_description(result['review_text']['full_html'])
                        else:
                            review_text = ""

                        info_dict = {}        
                        info_dict['author_name'] = author_name
                        info_dict['personal_rating'] =  personal_rating             
                        info_dict["review_date"] = review_date
                        info_dict["review_text"] = review_text
                        info_dict["review_acquisition_date"] = review_acquisition_date
                        info_dict["google_url"] = url
                        info_dict["biz_id"] = biz_id
                        reviewData.append(info_dict)

                    next_page_token = json_data.get('next_page_token','').strip()
                    if not next_page_token:
                        break
                else:
                    break
        except:
            num+=1
            continue
        reviews_info_header = list(reviewData[0].keys())
        reviews_info_df = pd.DataFrame.from_records(reviewData,columns=reviews_info_header)
        reviews_info_df.to_csv(f'./data/reviews/restaurant/{file_name.replace("/","")[0:6]}.csv')
        print(str(num) + ' 完成店名(review)' + place_name)
        num += 1


# In[ ]:


if __name__ == '__main__':
    print('請確定該py檔與url的cvs檔案放在相同路徑')
    file = input('請輸入url檔案名稱(含完整副檔名)，例如: place_info.csv\n')
    df = pd.read_csv(file)
    time1 = time.time()
    get_review()
    print(f'執行總花費時間: {time.time() - time1}')
    input('任務完成，若要關閉該視窗請輸入ENTER.....')

