# -*- coding: utf-8 -*-


import requests
import os
#import folium
#import webbrowser
import pandas as pd
from datetime import datetime
import json

# make the required folder for the data collection

try:
    os.makedirs('data')
except FileExistsError:
    pass



def lon_lat_extractor(postcode):
    # make the dataset which has postcode and its corresponding lat/lon
    # Instantiate the geocoding from locationIq
    postcode_area_key_list = postcode.columns.values.tolist()
    postcode_area_key = {}
    for area_key in postcode_area_key_list:
        postcode_dict ={}
        for i in postcode[area_key].values.tolist():
            attribute = {}
            # provide the access key
            # pass in the postal code in order to fetch the details
            url = "http://api.postcodes.io/postcodes/{}".format(i)
            response = requests.get(url)
            output = response.json()
            try:
                place = output['result']['nuts']
                longitude = output['result']['longitude']
                latitude = output['result']['latitude']
                attribute['place'] = place
                attribute['longitude'] = longitude
                attribute['latitude'] = latitude
            except KeyError:
                place = "No Information Found"
                longitude = None
                latitude = None
                attribute['place'] = place
                attribute['longitude'] = longitude
                attribute['latitude'] = latitude
            postcode_dict[i] = attribute
            # generate the log file
            with open("log.txt","a+") as logfile:
                logfile.write("{}: The data for postcode {} has been downloaded. \n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),i))
            
        postcode_area_key[area_key] = postcode_dict
            # generate the jsonfile
        with open(r"data/postcode_area_key_{}.json".format(area_key),"w") as outfile:
            json.dump(postcode_area_key,outfile)

if __name__ == "__main__":
    # Read the dataset
    postcode = pd.read_csv("postcode.csv")
    lon_lat_extractor(postcode)
    
