import requests
import json
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

## Get Avg Temp Data
output = pd.DataFrame()
for x in np.append(np.arange(1,49),[50]):
    xml =  requests.get("https://www.ncdc.noaa.gov/cag/statewide/time-series/{}-tavg-12-12-1990-2020.xml?base_prd=true&begbaseyear=1901&endbaseyear=2000".format(x)).content.decode("utf-8")
    tree = ET.fromstring(xml)
    state = tree.find('description').find('title').text.split(',')[0]
    year = []
    temp = []
    tempDF = pd.DataFrame()
    for info in tree.findall('data'):
        year.append(info.find('date').text[:4])
        temp.append(info.find('value').text)
    tempDF['Year'] = year
    tempDF['Average_Temp'] = temp
    states = [state]*len(year)
    tempDF['State'] = states
    output = pd.concat([output, tempDF])

## Get Annnual Precip Data
rainout = pd.DataFrame()
for x in np.append(np.arange(1,49),[50]):
    xml =  requests.get("https://www.ncdc.noaa.gov/cag/statewide/time-series/{}-pcp-12-12-1990-2020.xml?base_prd=true&begbaseyear=1925&endbaseyear=2000".format(x)).content.decode("utf-8")
    tree = ET.fromstring(xml)
    state = tree.find('description').find('title').text.split(',')[0]
    year = []
    rain = []
    tempDF = pd.DataFrame()
    for info in tree.findall('data'):
        year.append(info.find('date').text[:4])
        rain.append(info.find('value').text)
    tempDF['Year'] = year
    tempDF['percipitation'] = rain
    states = [state]*len(year)
    tempDF['State'] = states
    rainout = pd.concat([rainout, tempDF])

## Combine and Save Data to CSV
new_df = pd.merge(output, rainout,  how='left', left_on=['Year','State'], right_on = ['Year','State'])
new_df.to_csv('weather.csv')