from flask import Flask, render_template, request
from flask_moment import Moment
from datetime import datetime
import pandas as pd
import random
import folium
from folium import plugins
import json
from folium import CustomIcon
import ast

app = Flask(__name__)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html',
                           page_header="page_header",
                           current_time=datetime.utcnow())


# practice start
@app.route('/arange', methods=['GET'])
def arange():
    return render_template('arange.html')

# practice start


@app.route('/map', methods=['POST'])
def map():
    df_a = pd.read_csv('attraction_info_final_1217.csv')
    df_r = pd.read_csv('place_info_final_1217.csv')
    # 判斷星期幾
    date = request.form.get('date')
    dt = datetime.strptime(date, "%Y-%m-%d")
    weekday = dt.isoweekday()
    if weekday == 1:
        df_a['Monday'] = df_a['monday'].apply(ast.literal_eval)
        df_expanded = df_a["Monday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Monday'] = df_r['monday'].apply(ast.literal_eval)
        df_expanded = df_r["Monday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)
    elif weekday == 2:
        df_a['Tuesday'] = df_a['tuesday'].apply(ast.literal_eval)
        df_expanded = df_a["Tuesday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Tuesday'] = df_r['tuesday'].apply(ast.literal_eval)
        df_expanded = df_r["Tuesday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)
    elif weekday == 3:
        df_a['Wednesday'] = df_a['wednesday'].apply(ast.literal_eval)
        df_expanded = df_a["Wednesday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Wednesday'] = df_r['wednesday'].apply(ast.literal_eval)
        df_expanded = df_r["Wednesday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)
    elif weekday == 4:
        df_a['Thursday'] = df_a['thursday'].apply(ast.literal_eval)
        df_expanded = df_a["Thursday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Thursday'] = df_r['thursday'].apply(ast.literal_eval)
        df_expanded = df_r["Thursday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)
    elif weekday == 5:
        df_a['Friday'] = df_a['friday'].apply(ast.literal_eval)
        df_expanded = df_a["Friday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Friday'] = df_r['friday'].apply(ast.literal_eval)
        df_expanded = df_r["Friday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)
    elif weekday == 6:
        df_a['Saturday'] = df_a['saturday'].apply(ast.literal_eval)
        df_expanded = df_a["Saturday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Saturday'] = df_r['saturday'].apply(ast.literal_eval)
        df_expanded = df_r["Saturday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)
    elif weekday == 7:
        df_a['Sunday'] = df_a['sunday'].apply(ast.literal_eval)
        df_expanded = df_a["Sunday"].apply(pd.Series)
        df_a = pd.concat([df_a, df_expanded.iloc[:, 0:24]], axis=1)
        df_r['Sunday'] = df_r['sunday'].apply(ast.literal_eval)
        df_expanded = df_r["Sunday"].apply(pd.Series)
        df_r = pd.concat([df_r, df_expanded.iloc[:, 0:24]], axis=1)

    df_a_nightview = df_a[df_a['new_place_category'] == '夜景']
    df_a2 = df_a.drop(df_a_nightview.index)

    district = ["1", "2", "3", "4", "5"]
    # Weights for each item
    weights = [0.15, 0.1, 0.15, 0.35, 0.25]
    # Select a random item from the list, with the weights specified
    selected_district = random.choices(district, weights=weights)[0]

    # 建立空的 DataFrame 存放最終行程順序
    df = pd.DataFrame()

    # 篩選被挑選出的行政區的所有景點
    df_a2 = df_a2[df_a2['district_num'] == int(selected_district)]

    # 將rating大於4.3的*2, 小於3.7的/2 存到 rating2
    df_a2['rating2'] = df_a2['total_rating'].apply(
        lambda x: x*2 if x >= 4.3 else (x/2 if x <= 3.7 else x))
    df_a2['weights'] = df_a2['rating2'] / df_a2['rating2'].sum()

    # 隨機取樣一行
    attraction_1 = df_a2.sample(n=1, weights=df_a2['weights'])

    # 從原始df_a2中移除attraction_1的行
    df_a2 = df_a2.drop(attraction_1.index)

    # 隨機取樣一行
    attraction_2 = df_a2.sample(n=1, weights=df_a2['weights'])
    df_a2 = df_a2.drop(attraction_2.index)
    # result = pd.concat([result, attraction_2])

    d_latitude = (attraction_1['latitude'].values -
                  attraction_2['latitude'].values)[0]
    d_longitude = (attraction_1['longitude'].values -
                   attraction_2['longitude'].values)[0]

    def place_filter(data, filter1, filter2, filter3):
        df_in_func = data[filter1]
        if df_in_func.shape[0] != 0:
            df_in_func['rating2'] = df_in_func['total_rating'].apply(
                lambda x: x*2 if x >= 4.3 else (x/2 if x <= 3.7 else x))
            df_in_func['weights'] = df_in_func['rating2'] / \
                df_in_func['rating2'].sum()
            data_result = df_in_func.sample(n=1, weights=df_in_func['weights'])
        else:
            df_in_func = data[filter2]
            if df_in_func.shape[0] != 0:
                df_in_func['rating2'] = df_in_func['total_rating'].apply(
                    lambda x: x*2 if x >= 4.3 else (x/2 if x <= 3.7 else x))
                df_in_func['weights'] = df_in_func['rating2'] / \
                    df_in_func['rating2'].sum()
                data_result = df_in_func.sample(
                    n=1, weights=df_in_func['weights'])
            else:
                df_in_func = data[filter3]
                df_in_func['rating2'] = df_in_func['total_rating'].apply(
                    lambda x: x*2 if x >= 4.3 else (x/2 if x <= 3.7 else x))
                df_in_func['weights'] = df_in_func['rating2'] / \
                    df_in_func['rating2'].sum()
                data_result = df_in_func.sample(
                    n=1, weights=df_in_func['weights'])
        return data_result

    if abs(d_latitude) > abs(d_longitude):
        # 緯度差距大於精度差距，以緯度分割
        if d_latitude > 0:
            # 如果attraction_1在attraction_2的上面

            # 早餐店要篩選latitude > attraction_1的latitude
            filt_r_1 = (df_r['new_place_category'] == '早午餐') & (
                df_r['latitude'] > attraction_1['latitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            filt_r_1_2 = (df_r['new_place_category'] == '早午餐') & (
                df_r['latitude'] < attraction_1['latitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r['latitude'] > attraction_2['latitude'].values[0]) & (df_r[8] == 1)
            filt_r_1_3 = (df_r['new_place_category'] == '早午餐') & (
                df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            restaurant_1 = place_filter(df_r, filt_r_1, filt_r_1_2, filt_r_1_3)

            # category_list 接收回傳值
            category_list = request.form.getlist('food')
            if '咖啡甜點' in category_list:
                category_list_new = category_list.copy()
                category_list_new.remove('咖啡甜點')
            else:
                category_list_new = category_list.copy()
            # 午餐要選在attraction_1['latitude'] attraction_2['latitude']中間，且符合使用者選擇的類別
            filt_r_2 = (df_r['new_place_category'].isin(category_list_new)) & (attraction_1['latitude'].values[0]
                                                                               > df_r['latitude']) & (attraction_2['latitude'].values[0] < df_r['latitude']) & (df_r['district_num'] == int(selected_district)) & (df_r[11] == 1)
            filt_r_2_2 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['latitude'].values[0] < df_r['latitude']) & (df_r[11] == 1)
            filt_r_2_3 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['latitude'].values[0] > df_r['latitude']) & (df_r[11] == 1)
            restaurant_2 = place_filter(df_r, filt_r_2, filt_r_2_2, filt_r_2_3)
            df_r = df_r.drop(restaurant_2.index)

            # 景點3要篩選latitude < attraction_2的latitude
            if '咖啡甜點' in category_list:
                filt_r_3 = (df_r['latitude'] < attraction_2['latitude'].values[0]) & (
                    df_r['district_num'] == int(selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                filt_r_3_2 = (df_r['latitude'] > attraction_2['latitude'].values[0]) & (df_r['district_num'] == int(
                    selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r['latitude'] < attraction_1['latitude'].values[0]) & (df_r[15] == 1)
                filt_r_3_3 = (df_r['district_num'] == int(selected_district)) & (
                    df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_r, filt_r_3, filt_r_3_2, filt_r_3_3)
            else:
                filt_a_3 = (df_a2['latitude'] < attraction_2['latitude'].values[0]) & (
                    df_a2['district_num'] == int(selected_district)) & (df_a2[15] == 1)
                filt_a_3_2 = (df_a2['latitude'] > attraction_2['latitude'].values[0]) & (df_a2['district_num'] == int(
                    selected_district)) & (df_a2['latitude'] < attraction_1['latitude'].values[0]) & (df_a2[15] == 1)
                filt_a_3_3 = (df_a2['district_num'] == int(
                    selected_district)) & (df_a2[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_a2, filt_a_3, filt_a_3_2, filt_a_3_3)

        else:
            # 如果attraction_1在attraction_2的下面
            # 早餐店要篩選latitude < attraction_1的latitude
            filt_r_1 = (df_r['new_place_category'] == '早午餐') & (
                df_r['latitude'] < attraction_1['latitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            filt_r_1_2 = (df_r['new_place_category'] == '早午餐') & (
                df_r['latitude'] > attraction_1['latitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r['latitude'] < attraction_2['latitude'].values[0]) & (df_r[8] == 1)
            filt_r_1_3 = (df_r['new_place_category'] == '早午餐') & (
                df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            restaurant_1 = place_filter(df_r, filt_r_1, filt_r_1_2, filt_r_1_3)

            # category_list 接收回傳值
            category_list = request.form.getlist('food')
            if '咖啡甜點' in category_list:
                category_list_new = category_list.copy()
                category_list_new.remove('咖啡甜點')
            else:
                category_list_new = category_list.copy()

            # 午餐要選在attraction_1['latitude'] attraction_2['latitude']中間，且符合使用者選擇的類別
            filt_r_2 = (df_r['new_place_category'].isin(category_list_new)) & (attraction_1['latitude'].values[0]
                                                                               < df_r['latitude']) & (attraction_2['latitude'].values[0] > df_r['latitude']) & (df_r['district_num'] == int(selected_district)) & (df_r[11] == 1)
            filt_r_2_2 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['latitude'].values[0] > df_r['latitude']) & (df_r[11] == 1)
            filt_r_2_3 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['latitude'].values[0] < df_r['latitude']) & (df_r[11] == 1)
            restaurant_2 = place_filter(df_r, filt_r_2, filt_r_2_2, filt_r_2_3)
            df_r = df_r.drop(restaurant_2.index)

            # 景點3要篩選latitude > attraction_2的latitude
            if '咖啡甜點' in category_list:
                filt_r_3 = (df_r['latitude'] > attraction_2['latitude'].values[0]) & (
                    df_r['district_num'] == int(selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                filt_r_3_2 = (df_r['latitude'] < attraction_2['latitude'].values[0]) & (df_r['district_num'] == int(
                    selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r['latitude'] > attraction_1['latitude'].values[0]) & (df_r[15] == 1)
                filt_r_3_3 = (df_r['district_num'] == int(selected_district)) & (
                    df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_r, filt_r_3, filt_r_3_2, filt_r_3_3)
            else:
                filt_a_3 = (df_a2['latitude'] > attraction_2['latitude'].values[0]) & (
                    df_a2['district_num'] == int(selected_district)) & (df_a2[15] == 1)
                filt_a_3_2 = (df_a2['latitude'] < attraction_2['latitude'].values[0]) & (df_a2['district_num'] == int(
                    selected_district)) & (df_a2['latitude'] > attraction_1['latitude'].values[0]) & (df_a2[15] == 1)
                filt_a_3_3 = (df_a2['district_num'] == int(
                    selected_district)) & (df_a2[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_a2, filt_a_3, filt_a_3_2, filt_a_3_3)

    else:
        # 經度差距大於緯度差距，以經度分割
        if d_longitude > 0:
            # 早餐店要篩選longitude > attraction_1的longitude
            filt_r_1 = (df_r['new_place_category'] == '早午餐') & (
                df_r['longitude'] > attraction_1['longitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            filt_r_1_2 = (df_r['new_place_category'] == '早午餐') & (
                df_r['longitude'] < attraction_1['longitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r['longitude'] > attraction_2['longitude'].values[0]) & (df_r[8] == 1)
            filt_r_1_3 = (df_r['new_place_category'] == '早午餐') & (
                df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            restaurant_1 = place_filter(df_r, filt_r_1, filt_r_1_2, filt_r_1_3)

            # category_list 接收回傳值
            category_list = request.form.getlist('food')
            if '咖啡甜點' in category_list:
                category_list_new = category_list.copy()
                category_list_new.remove('咖啡甜點')
            else:
                category_list_new = category_list.copy()

            # 午餐要選在attraction_1['longitude'] attraction_2['longitude']中間，且符合使用者選擇的類別
            filt_r_2 = (df_r['new_place_category'].isin(category_list_new)) & (attraction_1['longitude'].values[0]
                                                                               > df_r['longitude']) & (attraction_2['longitude'].values[0] < df_r['longitude']) & (df_r['district_num'] == int(selected_district)) & (df_r[11] == 1)
            filt_r_2_2 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['longitude'].values[0] < df_r['longitude']) & (df_r[11] == 1)
            filt_r_2_3 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['longitude'].values[0] > df_r['longitude']) & (df_r[11] == 1)
            restaurant_2 = place_filter(df_r, filt_r_2, filt_r_2_2, filt_r_2_3)
            df_r = df_r.drop(restaurant_2.index)

            # 景點3要篩選longitude < attraction_2的longitude
            if '咖啡甜點' in category_list:
                filt_r_3 = (df_r['longitude'] < attraction_2['longitude'].values[0]) & (
                    df_r['district_num'] == int(selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                filt_r_3_2 = (df_r['longitude'] > attraction_2['longitude'].values[0]) & (df_r['district_num'] == int(
                    selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r['longitude'] < attraction_1['longitude'].values[0]) & (df_r[15] == 1)
                filt_r_3_3 = (df_r['district_num'] == int(selected_district)) & (
                    df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_r, filt_r_3, filt_r_3_2, filt_r_3_3)
            else:
                filt_a_3 = (df_a2['longitude'] < attraction_2['longitude'].values[0]) & (
                    df_a2['district_num'] == int(selected_district)) & (df_a2[15] == 1)
                filt_a_3_2 = (df_a2['longitude'] > attraction_2['longitude'].values[0]) & (df_a2['district_num'] == int(
                    selected_district)) & (df_a2['longitude'] < attraction_1['longitude'].values[0]) & (df_a2[15] == 1)
                filt_a_3_3 = (df_a2['district_num'] == int(
                    selected_district)) & (df_a2[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_a2, filt_a_3, filt_a_3_2, filt_a_3_3)
        else:
            # 如果attraction_1在attraction_2的下面
            # 早餐店要篩選longitude < attraction_1的longitude
            filt_r_1 = (df_r['new_place_category'] == '早午餐') & (
                df_r['longitude'] < attraction_1['longitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            filt_r_1_2 = (df_r['new_place_category'] == '早午餐') & (
                df_r['longitude'] > attraction_1['longitude'].values[0]) & (df_r['district_num'] == int(selected_district)) & (df_r['longitude'] < attraction_2['longitude'].values[0]) & (df_r[8] == 1)
            filt_r_1_3 = (df_r['new_place_category'] == '早午餐') & (
                df_r['district_num'] == int(selected_district)) & (df_r[8] == 1)
            restaurant_1 = place_filter(df_r, filt_r_1, filt_r_1_2, filt_r_1_3)

            # category_list 接收回傳值
            category_list = request.form.getlist('food')
            if '咖啡甜點' in category_list:
                category_list_new = category_list.copy()
                category_list_new.remove('咖啡甜點')
            else:
                category_list_new = category_list.copy()

            # 午餐要選在attraction_1['longitude'] attraction_2['longitude']中間，且符合使用者選擇的類別
            filt_r_2 = (df_r['new_place_category'].isin(category_list_new)) & (attraction_1['longitude'].values[0]
                                                                               < df_r['longitude']) & (attraction_2['longitude'].values[0] > df_r['longitude']) & (df_r['district_num'] == int(selected_district)) & (df_r[11] == 1)
            filt_r_2_2 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['longitude'].values[0] > df_r['longitude']) & (df_r[11] == 1)
            filt_r_2_3 = (df_r['new_place_category'].isin(category_list_new)) & (df_r['district_num'] == int(
                selected_district)) & (attraction_2['longitude'].values[0] < df_r['longitude']) & (df_r[11] == 1)
            restaurant_2 = place_filter(df_r, filt_r_2, filt_r_2_2, filt_r_2_3)
            df_r = df_r.drop(restaurant_2.index)

            # 景點3要篩選longitude > attraction_2的longitude
            if '咖啡甜點' in category_list:
                filt_r_3 = (df_r['longitude'] > attraction_2['longitude'].values[0]) & (
                    df_r['district_num'] == int(selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                filt_r_3_2 = (df_r['longitude'] < attraction_2['longitude'].values[0]) & (df_r['district_num'] == int(
                    selected_district)) & (df_r['new_place_category'] == '咖啡甜點') & (df_r['longitude'] > attraction_1['longitude'].values[0]) & (df_r[15] == 1)
                filt_r_3_3 = (df_r['district_num'] == int(selected_district)) & (
                    df_r['new_place_category'] == '咖啡甜點') & (df_r[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_r, filt_r_3, filt_r_3_2, filt_r_3_3)
            else:
                filt_a_3 = (df_a2['longitude'] > attraction_2['longitude'].values[0]) & (
                    df_a2['district_num'] == int(selected_district)) & (df_a2[15] == 1)
                filt_a_3_2 = (df_a2['longitude'] < attraction_2['longitude'].values[0]) & (df_a2['district_num'] == int(
                    selected_district)) & (df_a2['longitude'] > attraction_1['longitude'].values[0]) & (df_a2[15] == 1)
                filt_a_3_3 = (df_a2['district_num'] == int(
                    selected_district)) & (df_a2[15] == 1)
                restaurant_attraction_3 = place_filter(
                    df_a2, filt_a_3, filt_a_3_2, filt_a_3_3)

    # 選夜市、餐酒館、餐廳
    r4_list = category_list_new + ['夜市', '酒吧/餐酒館']
    filt_r_4 = (df_r['new_place_category'].isin(r4_list)) & (
        df_r['district_num'] == int(selected_district)) & (df_r[17] == 1)
    filt_r_4_2 = (df_r['new_place_category'].isin(r4_list)) & (
        df_r['district_num'] == int(selected_district)) & (df_r[17] == 1)
    filt_r_4_3 = (df_r['new_place_category'].isin(r4_list)) & (
        df_r['district_num'] == int(selected_district)) & (df_r[17] == 1)
    restaurant_4 = place_filter(df_r, filt_r_4, filt_r_4_2, filt_r_4_3)

    if restaurant_4['new_place_category'].values == '酒吧/餐酒館':
        filt_5 = (df_a_nightview['district_num'] == int(selected_district))
        restaurant_attraction_5 = place_filter(
            df_a_nightview, filt_5, filt_5, filt_5)
    else:
        if request.form.get('bar') == "1":
            filt_5 = (df_r['new_place_category'] == '酒吧/餐酒館') & (
                df_r['district_num'] == int(selected_district)) & (df_r[20] == 1)
            restaurant_attraction_5 = place_filter(
                df_r, filt_5, filt_5, filt_5)
        else:
            filt_5 = (df_a_nightview['district_num'] == int(selected_district))
            restaurant_attraction_5 = place_filter(
                df_a_nightview, filt_5, filt_5, filt_5)

    df = pd.concat([df, restaurant_1])
    df = pd.concat([df, attraction_1])
    df = pd.concat([df, restaurant_2])
    df = pd.concat([df, attraction_2])
    df = pd.concat([df, restaurant_attraction_3])
    df = pd.concat([df, restaurant_4])
    df = pd.concat([df, restaurant_attraction_5])

    start = int(request.form.get('start_time'))
    end = int(request.form.get('end_time'))
    if start >= 20:
        start_1 = 6
    elif start >= 18:
        start_1 = 5
    elif start >= 16:
        start_1 = 4
    elif start >= 14:
        start_1 = 3
    elif start >= 12:
        start_1 = 2
    elif start >= 10:
        start_1 = 1
    else:
        start_1 = 0

    if end >= 20:
        end_1 = 7
    elif end >= 18:
        end_1 = 6
    elif end >= 16:
        end_1 = 5
    elif end >= 14:
        end_1 = 4
    elif end >= 12:
        end_1 = 3
    elif end >= 10:
        end_1 = 2
    else:
        end_1 = 1
    
    df = df[start_1:end_1]
    # 最後合併完 reset index
    df = df.reset_index(drop=True)

    m = folium.Map(tiles="OpenStreetMap", location=[
                   df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)
    # marker_cluster = plugins.MarkerCluster().add_to(m)

    for i in range(len(df)):
        html = f"""
            <h2>{df.iloc[i]['place_name']}</h2>
            <p>Infomation:</p> 
            <ul>
            <li>總評論數: <span style="color: red; font-weight:bold;">{int(df.loc[i,'total_reviews'])}</span> 筆</li>
            <li>平均星數: <span style="color: red; font-weight:bold;">{df.loc[i,'total_rating']}</span></li>
            <li>地址: {df.loc[i,'address']}</li>
            </ul>
            </p>
            <p>Google Maps <a href="{df.iloc[i]['google_url']}" target = "_blank">link </a></p>
            """
        points = list(zip(df['latitude'], df['longitude']))
        iframe = folium.IFrame(html=html, width=300, height=250)
        popup = folium.Popup(iframe, max_width=2650)
        if i == 0:
            icon = CustomIcon('icon2.png', icon_size=(
                40, 40), icon_anchor=(20, 40))
        else:
            icon = CustomIcon('icon.png', icon_size=(
                40, 40), icon_anchor=(20, 40))

        folium.Marker(
            location=[df.iloc[i]['latitude'],
                      df.iloc[i]['longitude']], icon=icon,
            popup=popup,
            #         icon=folium.DivIcon(html=f"""
            #             <div><svg>
            #                 <circle cx="5" cy="5" r="4" fill="#69b3a2" opacity="0.7"/>
            #                 <rect x="3", y="3" width="3" height="3", fill="red", opacity=".7"
            #             </svg></div>""")
        ).add_to(m)
        folium.PolyLine(points, color='red', weight=2.5, opacity=1,
                        dash_array='4, 8', popup='Line').add_to(m)
    with open("台北界線.json", encoding='utf-8') as file:
        data = json.load(file)

    m.add_child(folium.GeoJson(data=data))

    m.save('./templates/parts/test_map4.html')
    return render_template('map.html', df=df)


@app.route('/final_map')
def final_map():
    return render_template('parts/test_map4.html', title='Map')


@app.route('/form_result', methods=['POST'])  # default methods is "GET"
def form_result():
    # List of items
    items = ["1", "2", "3", "4", "5"]
    # Weights for each item
    weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    # Select a random item from the list, with the weights specified
    selected_item = random.choices(items, weights=weights)[0]

    df = pd.read_csv('./static/a_cool2.csv')
    df2 = df[df['district_block'] == int(selected_item)]
    selected_rows = df2.sample(n=2)
    data2 = selected_rows['place_name']
    data2_value = data2.values
    data2 = data2_value.tolist()
    data3 = data2[0]
    data4 = data2[1]

    data = [
        ["date:", request.form.get('date')],
        ["start_time:", request.form.get('start_time')],
        ["end_time:", request.form.get('end_time')],
        ["eat:", request.form.get('eat')],
        ["bar:", request.form.get('bar')],
        ["food type:", request.form.getlist('food')],

    ]
    return render_template('form_result(practice).html', page_header="Form data", data=data, data3=data3, data4=data4)
# practice end


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9000)
