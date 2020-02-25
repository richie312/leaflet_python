# -*- coding: utf-8 -*-
import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
import folium
import webbrowser
import pandas as pd
from datetime import datetime
import json
import os

postcode = pd.read_csv("postcode.csv")
data_folder = os.path.join(os.getcwd(),'data')
json_file_list = os.listdir(data_folder)



app = Flask(__name__)
app.config['DEBUG'] = True



@app.route('/')
def index():
    tooltip = 'clickme'
    # read the json file from the data folder
    for file_index in range(len(json_file_list)):
        with open(os.path.join(data_folder,json_file_list[file_index]),"r") as readfile:
            data = json.load(readfile)
        
        for area_key in list(data.keys()):
            postcode_list = list(data[area_key].keys())
            m = folium.Map(
                location=[data[area_key][postcode_list[0]]['latitude'],
                          data[area_key][postcode_list[0]]['longitude']],
                zoom_start=10,
                #tiles='Stamen Terrain'
            )
            # lat lon tuple 
            latlon = [(data[area_key][postcode_list[i]]['latitude'],data[area_key][postcode_list[i]]['longitude'],data[area_key][postcode_list[i]]['place']) for i in range(len(postcode_list))]
            for coordinates in latlon:
                try:
                    folium.Marker([coordinates[0],coordinates[1]], popup='<i>{}</i>'.format(coordinates[2]), tooltip=tooltip).add_to(m)
                except ValueError:
                    pass
    return m._repr_html_()





if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5002)