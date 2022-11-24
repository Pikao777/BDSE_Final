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

# In[2]:


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

def place_info():
    initialize_chrome()
    num = 9666
    for i in url_list:
        driver.get(i)
        time.sleep(0.1)
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        # 地點資訊區塊
        rating_and_review_div = soup.find('div',{'class':'k7jAl lJ3Kh miFGmb'})
        

        # 店名
        place_name = rating_and_review_div.find('div',{'jsan':re.compile("t-dgE5uNmzjiE,7.m6QErb,7.WNBkOb,0.aria-label,0.role")})
        place_name = place_name.get('aria-label','').strip()

        # 評論數
        total_reviews = rating_and_review_div.find('span',{'aria-label':re.compile("^\d.+ 則評論")})
        if total_reviews:
            total_reviews = total_reviews.get('aria-label','').strip()
            total_reviews = total_reviews.removesuffix('則評論').strip()
            total_reviews = total_reviews.replace(',', '')
        if not total_reviews:
            total_reviews = ""

        # 星級
        total_rating = rating_and_review_div.find('span',{'aria-label':re.compile("^\s+?\d+\.\d+ 星級")})
        if total_rating:
            total_rating = total_rating.get('aria-label','').strip() 
            total_rating = total_rating.removesuffix('星級').strip()
        if not total_rating:
            total_rating = ""

        # 標籤
        place_category = rating_and_review_div.find('button',{'jsaction':re.compile("pane.rating.category")})
        if place_category:
            place_category = place_category.getText()
        if not place_category:
            place_category = ""

        # 行政區
        district = rating_and_review_div.find('button',{'data-tooltip':re.compile("複製 Plus Code")})
        if district:
            district = district.get('aria-label','').strip() 
            district = district.removesuffix('Plus Code: ').strip()
        if not district:
            district = ""

        # 內用
        eat_in = rating_and_review_div.find('div',{'aria-label':re.compile("提供內用")})
        if eat_in:
            eat_in = 1
        if not eat_in:
            eat_in = 0

        # 外帶
        to_go_1 = rating_and_review_div.find('div',{'aria-label':re.compile("提供外帶服務")})
        if to_go_1:
            to_go_1 = 1
        if not to_go_1:
            to_go_1 = 0

        # 路邊取餐
        to_go_2 = rating_and_review_div.find('div',{'aria-label':re.compile("提供路邊取餐服務")})
        if to_go_2:
            to_go_2 = 1
        if not to_go_2:
            to_go_2 = 0

        # 外送
        delivery = rating_and_review_div.find('div',{'aria-label':re.compile("提供外送服務")})
        if delivery:
            delivery = 1
        if not delivery:
            delivery = 0

        # 價位
        cost = rating_and_review_div.find('span',{'aria-label':re.compile("^價格")})
        if cost:
            cost = cost.getText()
        if not cost:
            cost = ""

        #  是否關閉
        close = rating_and_review_div.find('span',{'style':re.compile("color:#D93025")})
        if close:
            close = close.getText()
        if not close:
            close = ""    

        # 地址
        address = rating_and_review_div.find('button',{'aria-label':re.compile("^地址\:")})
        if address:
            address = address.get('aria-label','').strip() 
            address = address.removeprefix('地址:')      
        if not address:
            address = ""

        # 電話
        phone = rating_and_review_div.find('button',{'aria-label':re.compile("^電話號碼\:")})
        if phone:
            phone = phone.get('aria-label','').strip()    
            phone = phone.removeprefix('電話號碼:')
        if not phone:
            phone = ""

        # 營業時間
        opening_hours = rating_and_review_div.find('div',{'aria-label':re.compile("^星期")})
        if opening_hours:
            opening_hours = opening_hours.get('aria-label','')   
        if not opening_hours:
            opening_hours = ""

        # 網站
        website = rating_and_review_div.find('a',{'aria-label':re.compile("^網站\:")})
        if website:
            website = website.get('href')   
        if not website:
            website = ""

        # 獲取日期
        place_acquisition_date = datetime.now().strftime("%Y-%m-%d")
        
        # append place_info to dict
        info_dict = {}
        place_data = []
        info_dict['google_url'] = i
        info_dict['place_name'] = place_name
        if close == "永久停業" or close == "暫時關閉":
            info_dict["total_rating"] = None
        else:
            info_dict["total_rating"] = total_rating
        info_dict["place_category"] = place_category                                  
        info_dict['total_reviews'] =  total_reviews             
        info_dict['cost'] = cost
        info_dict['address'] =  address
        info_dict['district'] = district
        info_dict['eat_in'] = eat_in
        info_dict['to_go_1'] = to_go_1
        info_dict['to_go_2'] = to_go_2
        info_dict['delivery'] = delivery
        info_dict['opening_hours'] = opening_hours
        info_dict["website"] = website
        info_dict["phone"] = phone
        info_dict["close"] = close
        info_dict["place_acquisition_date"] = place_acquisition_date 
        place_data.append(info_dict)
        print(str(num) + ' 完成店名(info): ' + place_name)

        # save place_info to csv                                      
        place_info_header = list(place_data[0].keys())
        place_info_df = pd.DataFrame.from_records(place_data,columns=place_info_header)
        place_info_df.to_csv(f'./place_info.csv', mode='a', header=False)
        if close == "永久停業" or close == "暫時關閉":
            num += 1
            continue
        if total_reviews == "":
            num += 1
            continue
        
        # review區域
#         # 下一頁review內容的token(寫進url)
#         next_page_token = ""

#         # 設定biz_id(寫進url)
#         biz_id = re.search(r"1s(0.*?\:.*?)[^a-zA-Z\d\s:]",i) # 寫成迴圈的時候要改一下
#         if not biz_id:
#             print("Not a valid url.")
#         biz_id = biz_id.groups()[0]

#         reviewData = []
        
#         while True:
#             url = f'https://www.google.com/async/reviewSort?yv=3&async=feature_id:{biz_id},review_source:All%20reviews,sort_by:newestFirst,is_owner:false,filter_text:,associated_topic:,next_page_token:{next_page_token},_pms:s,_fmt:json'
#             response = requests.get(url)

#             response = response.text.removeprefix(")]}'")
#             json_data = json.loads(response)["localReviewsProto"]
            
#             if json_data.get('other_user_review'):
#                 review_data = json_data["other_user_review"]

#                 for result in review_data:
#                     personal_rating = result['star_rating']['value']
#                     author_name = result['author_real_name']
#                     review_date = result['publish_date']['localized_date']
#                     review_acquisition_date = datetime.now().strftime("%Y-%m-%d")
#                     if result.get('review_text'):
#                         review_text = parse_description(result['review_text']['full_html'])
#                     else:
#                         review_text = ""

#                     info_dict = {}        
#                     info_dict['author_name'] = author_name
#                     info_dict['personal_rating'] =  personal_rating             
#                     info_dict["review_date"] = review_date
#                     info_dict["review_text"] = review_text
#                     info_dict["review_acquisition_date"] = review_acquisition_date
#                     info_dict["google_url"] = i
#                     info_dict["biz_id"] = biz_id
#                     reviewData.append(info_dict)

#                 next_page_token = json_data.get('next_page_token','').strip()
#                 if not next_page_token:
#                     break
#             else:
#                 break
# #         if not json_data.get('other_user_review'):
# #             num += 1
# #             continue
            
#         reviews_info_header = list(reviewData[0].keys())
#         reviews_info_df = pd.DataFrame.from_records(reviewData,columns=reviews_info_header)
#         reviews_info_df.to_csv(f'./reviews/restaurant/{place_name.replace("/","")[0:8]}_review.csv')
#         print(str(num) + ' 完成店名(review)' + place_name)
        num += 1
    # 關閉瀏覽器
    driver.quit()


# In[3]:


if __name__ == '__main__':
    print('請確定該py檔與url的cvs檔案放在相同路徑')
    file = input('請輸入url檔案名稱(含完整副檔名)，例如: url.csv\n')
    df = pd.read_csv(file, header=None)
    url_list = df[0][9665:]
    time1 = time.time()
    place_info()
    print(f'執行總花費時間: {time.time() - time1}')
    input('任務完成，若要關閉該視窗請輸入ENTER.....')
    os._exit()

