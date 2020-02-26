# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,json
import folium
import pandas as pd
from datetime import datetime
import os

postcode = pd.read_csv("postcode.csv")
data_folder = os.path.join(os.getcwd(),'data')
json_file_list = os.listdir(data_folder)



app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/get_map',methods= ['GET','POST'])
def get_map():
    if request.method == 'POST':
        data = request.form
        print(data['Area_Key'])
        tooltip = 'clickme'
        # read the json file from the data folder
        data_folder = os.path.join(os.getcwd(),'data')
        json_file_list = os.listdir(data_folder)
        # get the keys from the file list
        downloaded_key_list = [json_file_list[i].split('_')[-1].split('.')[0] for i in range(len(json_file_list))]
        if data['Area_Key'] in downloaded_key_list:
            # load the specific file_data
            with open(os.path.join(data_folder,'postcode_area_key_{}.json'.format(data['Area_Key'])),"r") as readfile:
                map_data = json.load(readfile)
            # postcodes are the keys in the map_data dictionary
            postcode_list = list(map_data[data['Area_Key']].keys())
            m = folium.Map(
                    location=[map_data[data['Area_Key']][postcode_list[0]]['latitude'],
                    map_data[data['Area_Key']][postcode_list[0]]['longitude']],
                    zoom_start = 10,
                    # tiles='Stamen Terrain'
                    )
                # lat lon tuple 
            latlon = [(map_data[data['Area_Key']][postcode_list[i]]['latitude'],
                       map_data[data['Area_Key']][postcode_list[i]]['longitude'],
                       map_data[data['Area_Key']][postcode_list[i]]['place']) for i in range(len(postcode_list))]
            for coordinates in latlon:
                try:
                    folium.Marker([coordinates[0],coordinates[1]], popup='<i>{}</i>'.format(coordinates[2]), tooltip=tooltip).add_to(m)
                except ValueError:
                    pass
            map_folder = os.path.join(os.getcwd(),'templates')
            m.save(os.path.join(map_folder,'map.html'))
            # map the region with postcode area key;
            postcode_region = pd.read_csv("postcode_region.csv")
            msg = postcode_region['UK region'][postcode_region['Postcode prefix'] == data['Area_Key']].values[0]
            return render_template('index.html', msg = msg)
        else:
            msg = """The data for the postcode area key {} is either not a valid area code or not yet downloaded. """.format(data['Area_Key'])
            return render_template('index_404.html', msg = msg)
    else:
        return render_template('index.html')





if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5002)