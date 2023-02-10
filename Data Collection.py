#!/usr/bin/env python
# coding: utf-8

# In[23]:


# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)

# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)


# In[24]:


# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/" + str(x)).json()
            BoosterVersion.append(response['name'])


# In[76]:


# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])


# In[93]:


# Takes the dataset and uses the payloads column to call the API and append the list
def getPayloaddata(data):
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])


# In[110]:


#Takes the dataset and uses the cores column to call the API and append the data to the list
def getCoreData(data):
    for core in data['cores']:
        if core['core'] != None:
            response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])
        


# In[111]:


# Request rocket launch data from SpaceX API with url
spacex_url="https://api.spacexdata.com/v4/launches/past"


# In[112]:


response = requests.get(spacex_url)


# In[113]:


# Check the content of the response
print(response.content)


# In[114]:


static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'


# In[115]:


response.status_code #See if code was succesfull


# In[116]:


# Use json_normalize method to convert the json result into a dataframe
response.json()
data = pd.json_normalize(response.json())  


# In[117]:


data.head()


# In[118]:


# Take subset of our dataframe keeping only the features we want and the flight number and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]


# In[119]:


# Global Variables
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []


# In[120]:


BoosterVersion # see list is empty


# In[121]:


# Call getBosterVersion
getBoosterVersion(data)


# In[122]:


BoosterVersion[0:5]


# In[123]:


getLaunchSite(data)


# In[124]:


getPayloaddata(data)


# In[125]:


getCoreData(data)


# In[126]:


# Create a dictionary
launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}


# In[134]:


# Create a dataframe from the dictionary

data_launch =pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })


# In[146]:


# show head of dataframe
data_launch.head()


# In[139]:


# Filter dataframe to only include Falcon 9 launches

data_falcon9 = data_launch.loc[data_launch['BoosterVersion']!='Falcon 1']
data_falcon9


# In[140]:


# Reset Flight Number Column

data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
data_falcon9


# In[141]:


# check for null values in each column
data_falcon9.isnull().sum()


# In[143]:


# Use mean to replace missing values except in launching Pad  column will retain None values to represent when landing pads were not used.
mean=data_falcon9["PayloadMass"].mean()
data_falcon9['PayloadMass'].replace(np.nan,mean,inplace=True)
data_falcon9


# In[144]:


# Store as CSV
data_falcon9.to_csv('dataset_part_1.csv', index=False)


# In[ ]:




