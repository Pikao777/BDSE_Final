from flask import Flask, render_template, request
from flask_moment import Moment
from datetime import datetime
import pandas as pd
import random
import folium
from folium import plugins
import json


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


@app.route('/map', methods=['GET'])
def map():
    df = pd.read_csv('cool.csv')
    df = df[0:10]

    m = folium.Map(tiles="OpenStreetMap", location=[
                   df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)
    # marker_cluster = plugins.MarkerCluster().add_to(m)

    for i in range(len(df)):
        html = f"""
            <h2>{df.iloc[i]['place_name']}</h2>
            <p>Infomation:</p> 
            <ul>
            <li>總評論數: <span style="color: red; font-weight:bold;">{int(df.loc[i,'total_reviews'])}</span> 筆</li>
            <li>平均星數: <span style="color: red; font-weight:bold;">{int(df.loc[i,'total_rating'])}</span></li>
            <li>地址: {df.loc[i,'address']}</li>
            </ul>
            </p>
            <p>Google Maps <a href="{df.iloc[i]['google_url']}" target = "_blank">link </a></p>
            """

        iframe = folium.IFrame(html=html, width=300, height=250)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(
            location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],
            popup=popup,
            #         icon=folium.DivIcon(html=f"""
            #             <div><svg>
            #                 <circle cx="5" cy="5" r="4" fill="#69b3a2" opacity="0.7"/>
            #                 <rect x="3", y="3" width="3" height="3", fill="red", opacity=".7"
            #             </svg></div>""")
        ).add_to(m)

    with open("台北界線.json", encoding='utf-8') as file:
        data = json.load(file)

    m.add_child(folium.GeoJson(data=data))

    m.save('./templates/parts/test_map4.html')
    return render_template('map.html')


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
    app.run(debug=True)
